"""Staging-agnostic in-memory executor."""

from __future__ import annotations

import dataclasses
import datetime
import functools
import math
from collections.abc import Callable, Mapping, MutableMapping
from contextlib import AbstractContextManager, ExitStack, nullcontext
from types import TracebackType
from typing import Any, Final, cast

import numpy as np
import polars as pl
import polars.selectors as cs
import pyarrow as pa
import pyarrow.parquet as pq
import structlog
from google.protobuf import json_format, struct_pb2
from more_itertools import flatten
from typing_extensions import Self, deprecated

from corvic import embed, embedding_metric, op_graph, sql
from corvic.result import (
    InternalError,
    InvalidArgumentError,
    Ok,
    ResourceExhaustedError,
)
from corvic.system._dimension_reduction import DimensionReducer, UmapDimensionReducer
from corvic.system._embedder import (
    EmbedImageContext,
    EmbedTextContext,
    ImageEmbedder,
    TextEmbedder,
)
from corvic.system.op_graph_executor import (
    ExecutionContext,
    ExecutionResult,
    OpGraphExecutor,
    TableComputeContext,
    TableComputeResult,
    TableSliceArgs,
)
from corvic.system.staging import StagingDB
from corvic.system.storage import StorageManager
from corvic_generated.orm.v1 import table_pb2

_logger = structlog.get_logger()

"""Reference and Maximum number of years for normalizing year in Datetime encoder"""
REFERENCE_YEAR: Final = 1900
MAX_NUMBER_OF_YEARS: Final = 200

_MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY: Final = 3


def get_polars_embedding_length(
    embedding_df: pl.DataFrame, embedding_column_name: str
) -> Ok[int] | InvalidArgumentError:
    outer_type = embedding_df.schema[embedding_column_name]
    if isinstance(outer_type, pl.Array):
        return Ok(outer_type.shape[0])
    if not isinstance(outer_type, pl.List):
        return InvalidArgumentError("invalid embedding datatype", dtype=str(outer_type))
    if len(embedding_df[embedding_column_name]) == 0:
        return InvalidArgumentError(
            "cannot infer embedding length for empty embedding set"
        )
    embedding_length = len(embedding_df[embedding_column_name][0])
    if embedding_length < 1:
        return InvalidArgumentError("invalid embedding length", length=embedding_length)
    return Ok(embedding_length)


def get_polars_embedding(
    embedding_df: pl.DataFrame, embedding_column_name: str
) -> Ok[np.ndarray[Any, Any]] | InvalidArgumentError:
    outer_type = embedding_df.schema[embedding_column_name]
    if isinstance(outer_type, pl.Array):
        return Ok(embedding_df[embedding_column_name].to_numpy())
    if not isinstance(outer_type, pl.List):
        return InvalidArgumentError("invalid embedding datatype", dtype=str(outer_type))
    match get_polars_embedding_length(embedding_df, embedding_column_name):
        case Ok(embedding_length):
            pass
        case InvalidArgumentError() as err:
            return err
    return Ok(
        embedding_df[embedding_column_name]
        .cast(pl.Array(inner=outer_type.inner, shape=embedding_length))
        .to_numpy()
    )


@deprecated("use pa_scalar.batch_to_structs instead")
def batch_to_proto_struct(batch: pa.RecordBatch) -> list[struct_pb2.Struct]:
    """Converts a RecordBatch to protobuf Structs safely."""
    data = batch.to_pylist()
    structs = [struct_pb2.Struct() for _ in range(len(data))]
    for idx, datum in enumerate(data):
        make_dict_bytes_human_readable(datum)
        json_format.ParseDict(datum, structs[idx])
    return structs


def make_list_bytes_human_readable(data: list[Any]) -> None:
    """Utility function to cleanup list data types.

    This function ensures that the list can be converted to
    a protobuf Value safely.
    """
    for i in range(len(data)):
        match data[i]:
            case bytes():
                data[i] = data[i].decode("utf-8", errors="replace")
            case pl.Time() | pl.Date() | datetime.datetime() | datetime.date():
                data[i] = str(data[i])
            case dict():
                make_dict_bytes_human_readable(data[i])
            case list():
                make_list_bytes_human_readable(data[i])
            case _:
                pass


def make_dict_bytes_human_readable(data: MutableMapping[str, Any]) -> None:
    """Utility function to cleanup mapping data types.

    This function ensures that the mapping can be converted to
    a protobuf Value safely.
    """
    for k, v in data.items():
        match v:
            case bytes():
                data[k] = v.decode("utf-8", errors="replace")
            case pl.Time() | pl.Date() | datetime.datetime() | datetime.date():
                data[k] = str(v)
            case dict():
                make_dict_bytes_human_readable(data[k])
            case list():
                make_list_bytes_human_readable(data[k])
            case _:
                pass


def _as_df(
    batch_or_batch_container: pa.RecordBatchReader | pa.RecordBatch | _SchemaAndBatches,
    expected_schema: pa.Schema | None = None,
):
    expected_schema = expected_schema or batch_or_batch_container.schema
    schema_dataframe = cast(pl.DataFrame, pl.from_arrow(expected_schema.empty_table()))

    match batch_or_batch_container:
        case pa.RecordBatchReader():
            batches = list(batch_or_batch_container)
        case _SchemaAndBatches():
            batches = batch_or_batch_container.batches
        case pa.RecordBatch():
            batches = [batch_or_batch_container]

    if not batches:
        return schema_dataframe

    schema_dataframe = cast(pl.DataFrame, pl.from_arrow(batches[0]))

    return cast(
        pl.DataFrame,
        pl.from_arrow(batches, rechunk=False, schema=schema_dataframe.schema),
    )


@dataclasses.dataclass(frozen=True)
class _LazyFrameWithMetrics:
    data: pl.LazyFrame
    metrics: dict[str, Any]

    def apply(
        self, lf_op: Callable[[pl.LazyFrame], pl.LazyFrame]
    ) -> _LazyFrameWithMetrics:
        return _LazyFrameWithMetrics(lf_op(self.data), self.metrics)

    def with_data(self, data: pl.LazyFrame):
        return _LazyFrameWithMetrics(data, self.metrics)


@dataclasses.dataclass(frozen=True)
class _SchemaAndBatches:
    schema: pa.Schema
    batches: list[pa.RecordBatch]
    metrics: dict[str, Any]

    @classmethod
    def from_lazy_frame_with_metrics(cls, lfm: _LazyFrameWithMetrics):
        return cls.from_dataframe(lfm.data.collect(), lfm.metrics)

    def to_batch_reader(self):
        return pa.RecordBatchReader.from_batches(
            schema=self.schema,
            batches=self.batches or self.schema.empty_table().to_batches(),
        )

    @classmethod
    def from_dataframe(
        cls,
        dataframe: pl.DataFrame,
        metrics: dict[str, Any],
        expected_schema: pa.Schema | None = None,
    ):
        # it's hard to return an empty column from queries, this detects
        # tables that were supposed to be empty and works around them
        if (
            expected_schema is not None
            and len(expected_schema) == 0
            and not len(dataframe)
        ):
            return cls(expected_schema, [], metrics)
        table = dataframe.to_arrow()
        schema = table.schema
        return cls(schema, table.to_batches(), metrics)


@dataclasses.dataclass(frozen=True)
class _SlicedTable:
    op_graph: op_graph.Op
    slice_args: TableSliceArgs | None


@dataclasses.dataclass
class _InMemoryExecutionContext(AbstractContextManager["_InMemoryExecutionContext"]):
    exec_context: ExecutionContext
    current_output_context: TableComputeContext | None = None

    # Using _SchemaAndBatches rather than a RecordBatchReader since the latter's
    # contract only guarantees one iteration and these might be accessed more than
    # once
    computed_batches_for_op_graph: dict[_SlicedTable, _LazyFrameWithMetrics] = (
        dataclasses.field(default_factory=dict)
    )
    exit_stack: ExitStack = dataclasses.field(default_factory=ExitStack)

    def __enter__(self) -> Self:
        self.exit_stack = self.exit_stack.__enter__()
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        return self.exit_stack.__exit__(__exc_type, __exc_value, __traceback)

    @classmethod
    def count_source_op_uses(
        cls,
        op: op_graph.Op,
        use_counts: dict[_SlicedTable, int],
        slice_args: TableSliceArgs | None,
    ):
        for source in op.sources():
            sliced_table = _SlicedTable(source, slice_args)
            use_counts[sliced_table] = use_counts.get(sliced_table, 0) + 1
            cls.count_source_op_uses(source, use_counts, slice_args)

    @property
    def current_slice_args(self) -> TableSliceArgs | None:
        if self.current_output_context:
            return self.current_output_context.sql_output_slice_args
        return None

    @functools.cached_property
    def reused_tables(self) -> set[_SlicedTable]:
        use_counts = dict[_SlicedTable, int]()
        for output_table in self.output_tables:
            self.count_source_op_uses(
                output_table.op_graph, use_counts, output_table.slice_args
            )

        return {op for op, count in use_counts.items() if count > 1}

    @functools.cached_property
    def output_tables(self) -> set[_SlicedTable]:
        return {
            _SlicedTable(ctx.table_op_graph, ctx.sql_output_slice_args)
            for ctx in self.exec_context.tables_to_compute
        }


class InMemoryTableComputeResult(TableComputeResult):
    """The in-memory result of computing a particular op graph."""

    def __init__(
        self,
        storage_manager: StorageManager,
        batches: _SchemaAndBatches,
        context: TableComputeContext,
    ):
        self._storage_manager = storage_manager
        self._batches = batches
        self._context = context

    @property
    def metrics(self):
        return self._batches.metrics

    def to_batch_reader(self) -> pa.RecordBatchReader:
        return self._batches.to_batch_reader()

    def to_urls(self) -> list[str]:
        # one file for now; we may produce more in the future
        file_idx = 0
        file_name = f"{self._context.output_url_prefix}.{file_idx:>06}"
        with (
            self._storage_manager.blob_from_url(file_name).open("wb") as stream,
            pq.ParquetWriter(stream, self._batches.schema) as writer,
        ):
            for batch in self._batches.batches:
                writer.write_batch(batch)

        return [file_name]

    @property
    def context(self) -> TableComputeContext:
        return self._context


class InMemoryExecutionResult(ExecutionResult):
    """A container for in-memory results.

    This container is optimized to avoid writes to disk, i.e., `to_batch_reader` will
    be fast `to_urls` will be slow.
    """

    def __init__(
        self,
        tables: list[InMemoryTableComputeResult],
        context: ExecutionContext,
    ):
        self._tables = tables
        self._context = context

    @classmethod
    def make(
        cls,
        storage_manager: StorageManager,
        computed_tables: Mapping[_SlicedTable, _SchemaAndBatches],
        context: ExecutionContext,
    ) -> InMemoryExecutionResult:
        tables = [
            InMemoryTableComputeResult(
                storage_manager,
                computed_tables[
                    _SlicedTable(
                        table_context.table_op_graph,
                        table_context.sql_output_slice_args,
                    )
                ],
                table_context,
            )
            for table_context in context.tables_to_compute
        ]
        return InMemoryExecutionResult(
            tables,
            context,
        )

    @property
    def tables(self) -> list[InMemoryTableComputeResult]:
        return self._tables

    @property
    def context(self) -> ExecutionContext:
        return self._context


class InMemoryExecutor(OpGraphExecutor):
    """Executes op_graphs in memory (after staging queries)."""

    def __init__(
        self,
        staging_db: StagingDB,
        storage_manager: StorageManager,
        text_embedder: TextEmbedder,
        image_embedder: ImageEmbedder,
        dimension_reducer: DimensionReducer | None = None,
    ):
        self._staging_db = staging_db
        self._storage_manager = storage_manager
        self._text_embedder = text_embedder
        self._image_embedder = image_embedder
        self._dimension_reducer = dimension_reducer or UmapDimensionReducer()

    def _execute_read_from_parquet(
        self, op: op_graph.op.ReadFromParquet, context: _InMemoryExecutionContext
    ) -> Ok[_LazyFrameWithMetrics]:
        data = cast(pl.DataFrame, pl.from_arrow(op.arrow_schema.empty_table()))
        data = pl.scan_parquet(
            [
                context.exit_stack.enter_context(
                    self._storage_manager.blob_from_url(blob_name).open("rb")
                )
                for blob_name in op.blob_names
            ],
            schema=data.schema,
        )
        return Ok(_LazyFrameWithMetrics(data, metrics={}))

    def _execute_rollup_by_aggregation(
        self, op: op_graph.op.RollupByAggregation, context: _InMemoryExecutionContext
    ) -> Ok[_LazyFrameWithMetrics]:
        raise NotImplementedError(
            "rollup by aggregation outside of sql not implemented"
        )

    def _compute_source_then_apply(
        self,
        source: op_graph.Op,
        lf_op: Callable[[pl.LazyFrame], pl.LazyFrame],
        context: _InMemoryExecutionContext,
    ):
        return self._execute(source, context).map(
            lambda source_lfm: source_lfm.apply(lf_op)
        )

    def _execute_rename_columns(
        self, op: op_graph.op.RenameColumns, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.rename(dict(op.old_name_to_new)), context
        )

    def _execute_select_columns(
        self, op: op_graph.op.SelectColumns, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.select(op.columns), context
        )

    def _execute_limit_rows(
        self, op: op_graph.op.LimitRows, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.limit(op.num_rows), context
        )

    def _execute_offset_rows(
        self, op: op_graph.op.OffsetRows, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.slice(op.num_rows), context
        )

    def _execute_order_by(
        self, op: op_graph.op.OrderBy, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.sort(op.columns, descending=op.desc), context
        )

    def _row_filter_literal_comparison_to_condition(
        self, row_filter: op_graph.row_filter.CompareColumnToLiteral
    ) -> Ok[pl.Expr] | op_graph.OpParseError:
        # Cast to the expected polars type for comparisons.
        # This cast is not safe as there are literals that are
        # not pl.PythonLiterals (e.g., struct, map) which means
        # the below can fail at runtime with a cryptic error.
        lit = cast(Any, row_filter.literal_as_py)
        col = row_filter.column_name

        # Handle comparison with None/null separately
        if lit is None:
            match row_filter.comparison_type:
                case table_pb2.COMPARISON_TYPE_EQ:
                    comp = pl.col(col).is_null()
                case table_pb2.COMPARISON_TYPE_NE:
                    comp = pl.col(col).is_not_null()
                case _:
                    return op_graph.OpParseError(
                        "Unsupported literal None and comparison type",
                        value=row_filter.comparison_type,
                    )
        else:
            match row_filter.comparison_type:
                case table_pb2.COMPARISON_TYPE_EQ:
                    comp = pl.col(col) == lit
                case table_pb2.COMPARISON_TYPE_NE:
                    comp = pl.col(col) != lit
                case table_pb2.COMPARISON_TYPE_LT:
                    comp = pl.col(col) < lit
                case table_pb2.COMPARISON_TYPE_GT:
                    comp = pl.col(col) > lit
                case table_pb2.COMPARISON_TYPE_LE:
                    comp = pl.col(col) <= lit
                case table_pb2.COMPARISON_TYPE_GE:
                    comp = pl.col(col) >= lit
                case _:
                    return op_graph.OpParseError(
                        "unknown comparison type value in row filter",
                        value=row_filter.comparison_type,
                    )
        return Ok(comp)

    def _row_filter_combination_to_condition(
        self, row_filter: op_graph.row_filter.CombineFilters
    ) -> Ok[pl.Expr] | op_graph.OpParseError:
        sub_filters = list[pl.Expr]()
        for sub_filter in row_filter.row_filters:
            match self._row_filter_to_condition(sub_filter):
                case Ok(new_sub_filter):
                    sub_filters.append(new_sub_filter)
                case op_graph.OpParseError() as err:
                    return err
        match row_filter.combination_op:
            case table_pb2.LOGICAL_COMBINATION_ANY:
                return Ok(
                    functools.reduce(lambda left, right: left | right, sub_filters)
                )
            case table_pb2.LOGICAL_COMBINATION_ALL:
                return Ok(
                    functools.reduce(lambda left, right: left & right, sub_filters)
                )
            case _:
                return op_graph.OpParseError(
                    "unknown logical combination op value in row filter",
                    value=row_filter.combination_op,
                )

    def _row_filter_to_condition(
        self, row_filter: op_graph.RowFilter
    ) -> Ok[pl.Expr] | op_graph.OpParseError:
        match row_filter:
            case op_graph.row_filter.CompareColumnToLiteral():
                return self._row_filter_literal_comparison_to_condition(row_filter)
            case op_graph.row_filter.CombineFilters():
                return self._row_filter_combination_to_condition(row_filter)

    def _execute_filter_rows(
        self, op: op_graph.op.FilterRows, context: _InMemoryExecutionContext
    ):
        match self._row_filter_to_condition(op.row_filter):
            case op_graph.OpParseError() as err:
                return InternalError.from_(err)
            case Ok(row_filter):
                pass
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.filter(row_filter), context
        )

    def _execute_embedding_metrics(  # noqa: C901
        self, op: op_graph.op.EmbeddingMetrics, context: _InMemoryExecutionContext
    ):
        match self._execute(op.table, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        embedding_df = source_lfm.data.collect()

        if len(embedding_df) < _MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY:
            # downstream consumers handle empty metadata by substituting their
            # own values
            return Ok(
                _LazyFrameWithMetrics(embedding_df.lazy(), metrics=source_lfm.metrics)
            )

        # before it was configurable, this op assumed that the column's name was
        # this hardcoded name
        embedding_column_name = op.embedding_column_name or "embedding"
        match get_polars_embedding(embedding_df, embedding_column_name):
            case Ok(embedding):
                pass
            case InvalidArgumentError() as err:
                return InternalError.from_(err)

        metrics = source_lfm.metrics.copy()
        match embedding_metric.ne_sum(embedding, normalize=True):
            case Ok(metric):
                metrics["ne_sum"] = metric
            case InvalidArgumentError() as err:
                _logger.warning("could not compute ne_sum", exc_info=str(err))
        match embedding_metric.condition_number(embedding, normalize=True):
            case Ok(metric):
                metrics["condition_number"] = metric
            case InvalidArgumentError() as err:
                _logger.warning("could not compute condition_number", exc_info=str(err))
        match embedding_metric.rcondition_number(embedding, normalize=True):
            case Ok(metric):
                metrics["rcondition_number"] = metric
            case InvalidArgumentError() as err:
                _logger.warning(
                    "could not compute rcondition_number", exc_info=str(err)
                )
        match embedding_metric.stable_rank(embedding, normalize=True):
            case Ok(metric):
                metrics["stable_rank"] = metric
            case InvalidArgumentError() as err:
                _logger.warning("could not compute stable_rank", exc_info=str(err))
        return Ok(_LazyFrameWithMetrics(embedding_df.lazy(), metrics=metrics))

    def _execute_embedding_coordinates(
        self, op: op_graph.op.EmbeddingCoordinates, context: _InMemoryExecutionContext
    ):
        match self._execute(op.table, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        embedding_df = source_lfm.data.collect()

        # before it was configurable, this op assumed that the column's name was
        # this hardcoded name
        embedding_column_name = op.embedding_column_name or "embedding"

        # the neighbors of a point includes itself. That does mean, that an n_neighbors
        # value of less than 3 simply does not work
        if len(embedding_df) < _MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY:
            coordinates_df = embedding_df.lazy().with_columns(
                pl.Series(
                    name=embedding_column_name,
                    values=[[0.0] * op.n_components] * len(embedding_df),
                    dtype=pl.List(pl.Float32),
                )
            )
            return Ok(_LazyFrameWithMetrics(coordinates_df, source_lfm.metrics))

        match get_polars_embedding(embedding_df, embedding_column_name):
            case Ok(embedding):
                pass
            case InvalidArgumentError() as err:
                raise err

        match self._dimension_reducer.reduce_dimensions(
            embedding, op.n_components, op.metric
        ):
            case Ok(coordinates):
                pass
            case InvalidArgumentError() as err:
                raise err

        coordinates_df = embedding_df.lazy().with_columns(
            pl.Series(
                name=embedding_column_name,
                values=coordinates,
                dtype=pl.List(pl.Float32),
            )
        )
        return Ok(_LazyFrameWithMetrics(coordinates_df, source_lfm.metrics))

    def _execute_distinct_rows(
        self, op: op_graph.op.DistinctRows, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_lfm: _LazyFrameWithMetrics(
                source_lfm.data.unique(), source_lfm.metrics
            )
        )

    def _execute_join(self, op: op_graph.op.Join, context: _InMemoryExecutionContext):
        match self._execute(op.left_source, context):
            case Ok(left_lfm):
                pass
            case err:
                return err
        match self._execute(op.right_source, context):
            case Ok(right_lfm):
                pass
            case err:
                return err
        left_lf = left_lfm.data
        right_lf = right_lfm.data

        match op.how:
            case table_pb2.JOIN_TYPE_INNER:
                join_type = "inner"
            case table_pb2.JOIN_TYPE_LEFT_OUTER:
                join_type = "left"
            case _:
                join_type = "inner"

        # in our join semantics we drop columns from the right source on conflict
        right_lf = right_lf.select(
            [
                col
                for col in right_lf.columns
                if col in op.right_join_columns or col not in left_lf.columns
            ]
        )
        metrics = right_lfm.metrics.copy()
        metrics.update(left_lfm.metrics)

        return Ok(
            _LazyFrameWithMetrics(
                left_lf.join(
                    right_lf,
                    left_on=op.left_join_columns,
                    right_on=op.right_join_columns,
                    how=join_type,
                ),
                metrics,
            )
        )

    def _execute_empty(self, op: op_graph.op.Empty, context: _InMemoryExecutionContext):
        empty_table = cast(pl.DataFrame, pl.from_arrow(pa.schema([]).empty_table()))
        return Ok(_LazyFrameWithMetrics(empty_table.lazy(), metrics={}))

    def _execute_concat(
        self, op: op_graph.op.Concat, context: _InMemoryExecutionContext
    ):
        source_lfms = list[_LazyFrameWithMetrics]()
        for table in op.tables:
            match self._execute(table, context):
                case Ok(batches):
                    source_lfms.append(batches)
                case err:
                    return err
        data = pl.concat([lfm.data for lfm in source_lfms], how=op.how)
        metrics = dict[str, Any]()
        for lfm in source_lfms:
            metrics.update(lfm.metrics)
        return Ok(_LazyFrameWithMetrics(data, metrics=metrics))

    def _execute_unnest_struct(
        self, op: op_graph.op.UnnestStruct, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.unnest(op.struct_column_name), context
        )

    def _execute_nest_into_struct(
        self, op: op_graph.op.NestIntoStruct, context: _InMemoryExecutionContext
    ):
        non_struct_columns = [
            field.name
            for field in op.source.schema
            if field.name not in op.column_names_to_nest
        ]
        return self._compute_source_then_apply(
            op.source,
            lambda lf: lf.select(
                *non_struct_columns,
                pl.struct(op.column_names_to_nest).alias(op.struct_column_name),
            ),
            context,
        )

    def _execute_add_literal_column(
        self, op: op_graph.op.AddLiteralColumn, context: _InMemoryExecutionContext
    ):
        pl_schema = cast(
            pl.DataFrame, pl.from_arrow(op.column_arrow_schema.empty_table())
        ).schema
        name, dtype = next(iter(pl_schema.items()))

        literals = op.literals_as_py()
        if len(literals) == 1:
            column = pl.lit(literals[0]).cast(dtype).alias(name)
        else:
            column = pl.Series(name, literals).cast(dtype)

        return self._compute_source_then_apply(
            op.source,
            lambda lf: lf.with_columns(column),
            context,
        )

    def _execute_combine_columns(
        self, op: op_graph.op.CombineColumns, context: _InMemoryExecutionContext
    ):
        match op.reduction:
            case op_graph.ConcatString() as reduction:
                # if we do not ignore nulls then all concatenated rows that
                # have a single column that contain a null value will be output
                # as null.
                concat_expr = pl.concat_str(
                    [pl.col(col) for col in op.column_names],
                    separator=reduction.separator,
                    ignore_nulls=True,
                ).alias(op.combined_column_name)

            case op_graph.ConcatList():
                if op.column_names:
                    concat_expr = pl.concat_list(*op.column_names).alias(
                        op.combined_column_name
                    )
                else:
                    concat_expr = pl.Series(op.combined_column_name, [])

        return self._compute_source_then_apply(
            op.source,
            lambda lf: lf.with_columns(concat_expr),
            context,
        )

    def _execute_embed_column(
        self, op: op_graph.op.EmbedColumn, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        to_embed = source_df[op.column_name].cast(pl.String())

        embed_context = EmbedTextContext(
            inputs=to_embed,
            model_name=op.model_name,
            tokenizer_name=op.tokenizer_name,
            expected_vector_length=op.expected_vector_length,
            expected_coordinate_bitwidth=op.expected_coordinate_bitwidth,
            room_id=context.exec_context.room_id,
        )
        match self._text_embedder.embed(embed_context):
            case Ok(result):
                pass
            case InvalidArgumentError() | InternalError() as err:
                raise InternalError("Failed to embed column") from err

        result_df = (
            source_df.lazy()
            .with_columns(result.embeddings.alias(op.embedding_column_name))
            .drop_nulls(op.embedding_column_name)
        )

        return Ok(source_lfm.with_data(result_df))

    @staticmethod
    def get_cyclic_encoding(
        series: pl.Series,
        period: int,
    ) -> tuple[pl.Series, pl.Series]:
        sine_series = (2 * math.pi * series / period).sin().alias(f"{series.name}_sine")
        cosine_series = (
            (2 * math.pi * series / period).cos().alias(f"{series.name}_cosine")
        )
        return sine_series, cosine_series

    @staticmethod
    def encode_datetime(series: pl.Series) -> pl.Series:
        match series.dtype:
            case pl.Date | pl.Time:
                pass
            case pl.Datetime:
                series = series.dt.replace_time_zone("UTC")
            case _:
                raise ValueError("Invalid arguments, expected a datetime series")

        if series.is_null().all():
            zero_vector = pl.zeros(11, dtype=pl.Float32, eager=True)
            return pl.Series([zero_vector] * len(series), dtype=pl.List(pl.Float32))

        n = len(series)
        year_norm = pl.zeros(n, dtype=pl.Float32, eager=True).alias("year")
        month_sine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("month_sine")
        month_cosine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("month_cosine")
        day_sine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("day_sine")
        day_cosine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("day_cosine")
        hour_sine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("hour_sine")
        hour_cosine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("hour_cosine")
        minute_sine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("minute_sine")
        minute_cosine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("minute_cosine")
        second_sine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("second_sine")
        second_cosine = pl.zeros(n, dtype=pl.Float32, eager=True).alias("second_cosine")

        if series.dtype in [pl.Date, pl.Datetime]:
            try:
                year = series.dt.year().cast(pl.Float32).alias("year")
                month = series.dt.month().cast(pl.Float32).alias("month")
                day = series.dt.day().cast(pl.Float32).alias("day")

                year_norm = (year - REFERENCE_YEAR) / MAX_NUMBER_OF_YEARS
                month_sine, month_cosine = InMemoryExecutor.get_cyclic_encoding(
                    month, 12
                )
                day_sine, day_cosine = InMemoryExecutor.get_cyclic_encoding(day, 31)
            except pl.exceptions.PanicException as e:
                _logger.exception("Error extracting datetime", exc_info=e)

        if series.dtype in [pl.Time, pl.Datetime]:
            try:
                hour = series.dt.hour().cast(pl.Float32).alias("hour")
                minute = series.dt.minute().cast(pl.Float32).alias("minute")
                second = series.dt.second().cast(pl.Float32).alias("second")

                hour_sine, hour_cosine = InMemoryExecutor.get_cyclic_encoding(hour, 24)
                minute_sine, minute_cosine = InMemoryExecutor.get_cyclic_encoding(
                    minute, 60
                )
                second_sine, second_cosine = InMemoryExecutor.get_cyclic_encoding(
                    second, 60
                )
            except pl.exceptions.PanicException as e:
                _logger.exception("Error extracting datetime", exc_info=e)

        return pl.DataFrame(
            [
                year_norm.fill_null(0.0),
                month_sine.fill_null(0.0),
                month_cosine.fill_null(0.0),
                day_sine.fill_null(0.0),
                day_cosine.fill_null(0.0),
                hour_sine.fill_null(0.0),
                hour_cosine.fill_null(0.0),
                minute_sine.fill_null(0.0),
                minute_cosine.fill_null(0.0),
                second_sine.fill_null(0.0),
                second_cosine.fill_null(0.0),
            ]
        ).select(pl.concat_list(pl.all()).alias(series.name))[series.name]

    @staticmethod
    def encode_duration(series: pl.Series) -> pl.Series:
        if series.dtype != pl.Duration:
            raise ValueError("Invalid arguments, expected a duration series")
        if series.is_null().all():
            return pl.zeros(len(series), dtype=pl.Float32, eager=True)

        return series.dt.total_seconds().cast(pl.Float32).fill_null(0.0)

    @staticmethod
    def encode_text(series: pl.Series) -> pl.Series:
        match series.dtype:
            case pl.String:
                pass
            case pl.Binary:
                series = series.map_elements(
                    lambda x: x.decode("utf-8", errors="replace"),
                    return_dtype=pl.String,
                )
            case _:
                raise ValueError("Invalid arguments, expected a string series")
        series = series.fill_null(" ").replace("", " ")
        return pl.Series(
            series.name,
            [[1 / (len(doc) + 1)] for doc in series],
            pl.List(pl.Float32),
        )

    def _execute_encode_columns(  # noqa: C901, PLR0915
        self, op: op_graph.op.EncodeColumns, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        metrics = source_lfm.metrics.copy()
        metric = metrics.get("one_hot_encoder", {})
        for encoder_arg in op.encoded_columns:
            to_encode = source_df[encoder_arg.column_name]
            match encoder_arg.encoder:
                case op_graph.encoder.OneHotEncoder():
                    encoded = to_encode.to_dummies()
                    metric[encoder_arg.column_name] = encoded.columns
                    encoded = encoded.select(
                        pl.concat_list(pl.all())
                        .alias(encoder_arg.encoded_column_name)
                        .cast(pl.List(pl.Boolean))
                    )

                case op_graph.encoder.MinMaxScaler():
                    from sklearn.preprocessing import MinMaxScaler

                    encoder = MinMaxScaler(
                        feature_range=(
                            encoder_arg.encoder.feature_range_min,
                            encoder_arg.encoder.feature_range_max,
                        )
                    )
                    encoded = encoder.fit_transform(
                        to_encode.to_numpy().reshape(-1, 1)
                    ).flatten()

                case op_graph.encoder.LabelBinarizer():
                    from sklearn.preprocessing import LabelBinarizer

                    encoder = LabelBinarizer(
                        neg_label=encoder_arg.encoder.neg_label,
                        pos_label=encoder_arg.encoder.pos_label,
                    )
                    encoded = encoder.fit_transform(to_encode.to_numpy().reshape(-1))

                case op_graph.encoder.LabelEncoder():
                    from sklearn.preprocessing import LabelEncoder

                    encoder = LabelEncoder()
                    encoded = encoder.fit_transform(
                        to_encode.to_numpy().reshape(-1)
                    ).flatten()
                    # `classes_` is only set after fit,
                    # Creating custom typestubs will not solve this typing issue.
                    if encoder_arg.encoder.normalize and hasattr(encoder, "classes_"):
                        classes_ = cast(list[int], encoder.classes_)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
                        max_class: int = len(classes_) - 1
                        if max_class > 0:
                            encoded = encoded.astype(np.float64)
                            encoded /= max_class

                case op_graph.encoder.KBinsDiscretizer():
                    from sklearn.preprocessing import KBinsDiscretizer

                    encoder = KBinsDiscretizer(
                        n_bins=encoder_arg.encoder.n_bins,
                        encode=encoder_arg.encoder.encode_method,
                        strategy=encoder_arg.encoder.strategy,
                        dtype=np.float32,
                    )
                    encoded = encoder.fit_transform(
                        to_encode.to_numpy().reshape(-1, 1)
                    ).flatten()

                case op_graph.encoder.Binarizer():
                    from sklearn.preprocessing import Binarizer

                    encoder = Binarizer(
                        threshold=encoder_arg.encoder.threshold,
                    )
                    encoded = encoder.fit_transform(
                        to_encode.to_numpy().reshape(-1, 1)
                    ).flatten()

                case op_graph.encoder.MaxAbsScaler():
                    from sklearn.preprocessing import MaxAbsScaler

                    encoder = MaxAbsScaler()
                    try:
                        encoded = encoder.fit_transform(
                            np.nan_to_num(to_encode.to_numpy()).reshape(-1, 1)
                        ).flatten()
                    except ValueError:
                        encoded = np.array([])

                case op_graph.encoder.StandardScaler():
                    from sklearn.preprocessing import StandardScaler

                    encoder = StandardScaler(
                        with_mean=encoder_arg.encoder.with_mean,
                        with_std=encoder_arg.encoder.with_std,
                    )
                    encoded = encoder.fit_transform(
                        to_encode.to_numpy().reshape(-1, 1)
                    ).flatten()

                case op_graph.encoder.TimestampEncoder():
                    if to_encode.dtype == pl.datatypes.Duration:
                        encoded = self.encode_duration(to_encode)
                    else:
                        encoded = self.encode_datetime(to_encode)
                    source_df = source_df.with_columns(
                        encoded.rename(encoder_arg.encoded_column_name).cast(
                            encoder_arg.encoder.output_dtype
                        )
                    )
                    continue

                case op_graph.encoder.TextEncoder():
                    encoded = self.encode_text(to_encode)
                    source_df = source_df.with_columns(
                        encoded.rename(encoder_arg.encoded_column_name).cast(
                            encoder_arg.encoder.output_dtype
                        )
                    )
                    continue

            source_df = source_df.with_columns(
                pl.Series(
                    name=encoder_arg.encoded_column_name,
                    values=encoded,
                    dtype=encoder_arg.encoder.output_dtype,
                )
            )
        metrics["one_hot_encoder"] = metric
        return Ok(
            _LazyFrameWithMetrics(
                source_df.lazy(),
                metrics,
            )
        )

    def _execute_embed_node2vec_from_edge_lists(
        self,
        op: op_graph.op.EmbedNode2vecFromEdgeLists,
        context: _InMemoryExecutionContext,
    ):
        dtypes: set[pa.DataType] = set()
        entities_dtypes: dict[str, pa.DataType] = {}
        for edge_list in op.edge_list_tables:
            schema = edge_list.table.schema.to_arrow()
            start_dtype = schema.field(edge_list.start_column_name).type
            end_dtype = schema.field(edge_list.end_column_name).type
            dtypes.add(start_dtype)
            dtypes.add(end_dtype)
            entities_dtypes[edge_list.start_column_name] = start_dtype
            entities_dtypes[edge_list.end_column_name] = end_dtype

        start_fields = [pa.field(f"start_id_{dtype}", dtype) for dtype in dtypes]
        start_fields.append(pa.field("start_source", pa.large_string()))
        start_id_column_names = [field.name for field in start_fields]

        end_fields = [pa.field(f"end_id_{dtype}", dtype) for dtype in dtypes]
        end_fields.append(pa.field("end_source", pa.large_string()))
        end_id_column_names = [field.name for field in end_fields]

        fields = start_fields + end_fields
        empty_edges_table = pl.from_arrow(pa.schema(fields).empty_table())

        if isinstance(empty_edges_table, pl.Series):
            empty_edges_table = empty_edges_table.to_frame()

        metrics = dict[str, Any]()

        edge_list_lfms = list[_LazyFrameWithMetrics]()
        for edge_list in op.edge_list_tables:
            match self._execute(edge_list.table, context):
                case Ok(source_lfm):
                    edge_list_lfms.append(source_lfm)
                case err:
                    return err

        def edge_generator():
            for edge_list, lfm in zip(op.edge_list_tables, edge_list_lfms, strict=True):
                start_column_name = edge_list.start_column_name
                end_column_name = edge_list.end_column_name
                start_column_type_name = entities_dtypes[start_column_name]
                end_column_type_name = entities_dtypes[end_column_name]
                metrics.update(lfm.metrics)
                yield (
                    lfm.data.with_columns(
                        pl.col(edge_list.start_column_name).alias(
                            f"start_id_{start_column_type_name}"
                        ),
                        pl.lit(edge_list.start_entity_name).alias("start_source"),
                        pl.col(edge_list.end_column_name).alias(
                            f"end_id_{end_column_type_name}"
                        ),
                        pl.lit(edge_list.end_entity_name).alias("end_source"),
                    )
                    .select(
                        f"start_id_{start_column_type_name}",
                        "start_source",
                        f"end_id_{end_column_type_name}",
                        "end_source",
                    )
                    .collect()
                )

        edges = pl.concat(
            [
                empty_edges_table,
                *(edge_list for edge_list in edge_generator()),
            ],
            rechunk=False,
            how="diagonal",
        )

        n2v_space = embed.Space(
            edges=edges,
            start_id_column_names=start_id_column_names,
            end_id_column_names=end_id_column_names,
            directed=True,
        )
        n2v_runner = embed.Node2Vec(
            space=n2v_space,
            dim=op.ndim,
            walk_length=op.walk_length,
            window=op.window,
            p=op.p,
            q=op.q,
            alpha=op.alpha,
            min_alpha=op.min_alpha,
            negative=op.negative,
        )
        n2v_runner.train(epochs=op.epochs)
        return Ok(_LazyFrameWithMetrics(n2v_runner.wv.to_polars().lazy(), metrics))

    def _execute_aggregate_columns(
        self, op: op_graph.op.AggregateColumns, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        to_aggregate = source_lfm.data.select(op.column_names)

        match op.aggregation:
            case op_graph.aggregation.Min():
                aggregate = to_aggregate.min()
            case op_graph.aggregation.Max():
                aggregate = to_aggregate.max()
            case op_graph.aggregation.Mean():
                aggregate = to_aggregate.mean()
            case op_graph.aggregation.Std():
                aggregate = to_aggregate.std()
            case op_graph.aggregation.Quantile():
                aggregate = to_aggregate.quantile(op.aggregation.quantile)
            case op_graph.aggregation.Count():
                aggregate = to_aggregate.count()
            case op_graph.aggregation.NullCount():
                aggregate = to_aggregate.null_count()

        return Ok(source_lfm.with_data(aggregate))

    def _execute_correlate_columns(
        self, op: op_graph.op.CorrelateColumns, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        with np.errstate(invalid="ignore"):
            corr_df = source_df.select(op.column_names).corr(dtype="float32")

        return Ok(source_lfm.with_data(corr_df.lazy()))

    def _execute_histogram_column(
        self, op: op_graph.op.HistogramColumn, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source,
            lambda lf: lf.collect()[op.column_name]
            .hist(include_category=False)
            .lazy()
            .rename(
                {
                    "breakpoint": op.breakpoint_column_name,
                    "count": op.count_column_name,
                }
            ),
            context,
        )

    def _execute_convert_column_to_string(
        self, op: op_graph.op.ConvertColumnToString, context: _InMemoryExecutionContext
    ):
        dtype = op.source.schema.to_polars()[op.column_name]
        if not dtype.is_nested():
            cast_expr = pl.col(op.column_name).cast(pl.String(), strict=False)
        elif isinstance(dtype, pl.Array | pl.List):
            cast_expr = pl.col(op.column_name).cast(pl.List(pl.String())).list.join(",")
        else:
            raise NotImplementedError(
                "converting struct columns to strings is not implemented"
            )
        return self._compute_source_then_apply(
            op.source, lambda lf: lf.collect().with_columns(cast_expr).lazy(), context
        )

    def _execute_add_row_index(
        self, op: op_graph.op.AddRowIndex, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source,
            lambda lf: lf.with_row_index(
                name=op.row_index_column_name, offset=op.offset
            ).with_columns(pl.col(op.row_index_column_name).cast(pl.UInt64())),
            context,
        )

    def _execute_output_csv(
        self, op: op_graph.op.OutputCsv, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        source_df.write_csv(
            op.csv_url,
            quote_style="never",
            include_header=op.include_header,
        )
        return Ok(source_lfm.with_data(source_df.lazy()))

    def _execute_truncate_list(
        self, op: op_graph.op.TruncateList, context: _InMemoryExecutionContext
    ):
        # TODO(Patrick): verify this approach works for arrays
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        if len(source_df):
            existing_length = get_polars_embedding_length(
                source_df, op.column_name
            ).unwrap_or_raise()
        else:
            existing_length = 0
        head_length = (
            op.target_column_length
            if existing_length >= op.target_column_length
            else existing_length
        )
        source_df = source_df.with_columns(
            pl.col(op.column_name).list.head(head_length)
        )
        outer_type = source_df.schema[op.column_name]
        if isinstance(outer_type, pl.Array | pl.List):
            inner_type = outer_type.inner
        else:
            return InternalError("unexpected type", cause="expected list or array type")

        source_df = source_df.lazy()
        if head_length < op.target_column_length:
            padding_length = op.target_column_length - head_length
            padding = [op.padding_value_as_py] * padding_length
            source_df = source_df.with_columns(
                pl.col(op.column_name).list.concat(padding)
            )
        source_df = source_df.with_columns(
            pl.col(op.column_name)
            .list.to_array(width=op.target_column_length)
            .cast(pl.List(inner_type))
        )
        return Ok(source_lfm.with_data(source_df))

    def _execute_union(self, op: op_graph.op.Union, context: _InMemoryExecutionContext):
        sources = list[_LazyFrameWithMetrics]()
        for source in op.sources():
            match self._execute(source, context):
                case Ok(source_lfm):
                    sources.append(source_lfm)
                case err:
                    return err

        metrics = dict[str, Any]()
        for src in sources:
            metrics.update(src.metrics)

        result_lf = pl.concat((src.data for src in sources), how="vertical_relaxed")
        if op.distinct:
            result_lf = result_lf.unique()
        return Ok(_LazyFrameWithMetrics(result_lf, metrics=metrics))

    def _execute_embed_image_column(
        self, op: op_graph.op.EmbedImageColumn, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        to_embed = source_df[op.column_name].cast(pl.Binary())

        embed_context = EmbedImageContext(
            inputs=to_embed,
            model_name=op.model_name,
            expected_vector_length=op.expected_vector_length,
            expected_coordinate_bitwidth=op.expected_coordinate_bitwidth,
        )
        match self._image_embedder.embed(embed_context):
            case Ok(result):
                pass
            case InvalidArgumentError() | InternalError() as err:
                raise InternalError("Failed to embed column") from err

        return Ok(
            _LazyFrameWithMetrics(
                source_df.lazy()
                .with_columns(result.embeddings.alias(op.embedding_column_name))
                .drop_nulls(op.embedding_column_name),
                source_lfm.metrics,
            )
        )

    def _execute_add_decision_tree_summary(
        self, op: op_graph.op.AddDecisionTreeSummary, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err

        df_input = source_lfm.data.collect()
        dataframe = df_input.select(
            list({*op.feature_column_names, op.label_column_name})
        )
        boolean_columns = [
            name
            for name, dtype in dataframe.schema.items()
            if dtype == pl.Boolean() and name in op.feature_column_names
        ]

        # Drop Nan and Null and infinite rows as not supported by decision tree
        dataframe = dataframe.with_columns(
            *[pl.col(col).cast(pl.Float32) for col in op.feature_column_names]
        )
        dataframe = dataframe.drop_nans().drop_nulls()
        try:
            # is_infinite is not implemented for all datatypes
            dataframe = dataframe.filter(~pl.any_horizontal(cs.numeric().is_infinite()))
        except pl.exceptions.InvalidOperationError as err:
            return InvalidArgumentError.from_(err)

        if not len(dataframe):
            return InvalidArgumentError(
                "a minimum of 1 sample is required by DecisionTreeClassifier"
            )
        features = dataframe[op.feature_column_names]
        classes = dataframe[op.label_column_name]
        max_depth = op.max_depth

        from sklearn.tree import DecisionTreeClassifier, export_graphviz, export_text
        from sklearn.utils.multiclass import check_classification_targets

        try:
            check_classification_targets(classes)
        except ValueError as err:
            return InvalidArgumentError.from_(err)

        decision_tree = DecisionTreeClassifier(random_state=0, max_depth=max_depth)
        try:
            decision_tree.fit(features, classes)
        except (TypeError, ValueError) as err:
            return InternalError("cannot fit decision tree", exc=str(err))

        tree_str = export_text(
            decision_tree=decision_tree,
            feature_names=op.feature_column_names,
            class_names=op.classes_names,
            max_depth=max_depth,
        )

        tree_graphviz = export_graphviz(
            decision_tree=decision_tree,
            feature_names=op.feature_column_names,
            class_names=op.classes_names,
            max_depth=max_depth,
        )

        for boolean_column in boolean_columns:
            tree_str = tree_str.replace(
                f"{boolean_column} <= 0.50", f"NOT {boolean_column}"
            )
            tree_str = tree_str.replace(f"{boolean_column} >  0.50", boolean_column)

        metrics = source_lfm.metrics.copy()
        metrics[op.output_metric_key] = table_pb2.DecisionTreeSummary(
            text=tree_str, graphviz=tree_graphviz
        )
        return Ok(_LazyFrameWithMetrics(df_input.lazy(), metrics=metrics))

    def _execute_unnest_list(
        self, op: op_graph.op.UnnestList, context: _InMemoryExecutionContext
    ):
        return self._compute_source_then_apply(
            op.source,
            lambda lf: lf.with_columns(
                pl.col(op.list_column_name).list.get(i).alias(column_name)
                for i, column_name in enumerate(op.column_names)
            ).drop(op.list_column_name),
            context,
        )

    def _execute_sample_rows(
        self, op: op_graph.op.SampleRows, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        n = min(op.num_rows, source_df.shape[0])
        sample_strategy = op.sample_strategy
        match sample_strategy:
            case op_graph.sample_strategy.UniformRandom():
                result_df = source_df.sample(
                    n=n,
                    seed=sample_strategy.seed,
                )

        return Ok(
            _LazyFrameWithMetrics(
                result_df.lazy(),
                source_lfm.metrics,
            )
        )

    def _execute_describe_columns(
        self, op: op_graph.op.DescribeColumns, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case Ok(source_lfm):
                pass
            case err:
                return err
        source_df = source_lfm.data.collect()
        return Ok(
            source_lfm.with_data(
                source_df.describe()
                .lazy()
                .rename({"statistic": op.statistic_column_name})
            )
        )

    def _has_partially_computed_data(
        self, op: op_graph.Op, context: _InMemoryExecutionContext
    ) -> bool:
        return any(
            _SlicedTable(source, context.current_slice_args)
            in context.computed_batches_for_op_graph
            for source in op.sources()
        ) or any(
            self._has_partially_computed_data(sub_source, context)
            for sub_source in flatten(source.sources() for source in op.sources())
        )

    def _do_execute(  # noqa: C901
        self,
        op: op_graph.Op,
        context: _InMemoryExecutionContext,
    ) -> (
        Ok[_LazyFrameWithMetrics]
        | InternalError
        | ResourceExhaustedError
        | InvalidArgumentError
    ):
        if (
            not self._has_partially_computed_data(op, context)
            and sql.can_be_sql_computed(op, recursive=True)
            and self._staging_db
        ):
            expected_schema = op.schema.to_arrow()
            match sql.parse_op_graph(
                op,
                self._staging_db.query_for_blobs,
                self._staging_db.query_for_vector_search,
            ):
                case InvalidArgumentError() as err:
                    return InternalError.from_(err)
                case sql.NoRowsError() as err:
                    return Ok(
                        _LazyFrameWithMetrics(
                            cast(
                                pl.DataFrame,
                                pl.from_arrow(expected_schema.empty_table()),
                            ).lazy(),
                            metrics={},
                        )
                    )
                case Ok(query):
                    pass
            return self._staging_db.run_select_query(
                query, expected_schema, context.current_slice_args
            ).map(
                lambda rbr: _LazyFrameWithMetrics(
                    _as_df(rbr, expected_schema).lazy(),
                    metrics={},
                )
            )

        match op:
            case op_graph.op.SelectFromStaging():
                raise InternalError("SelectFromStaging should always be lowered to sql")
            case op_graph.op.SelectFromVectorStaging():
                raise InternalError(
                    "SelectFromVectorStaging should always be lowered to sql"
                )
            case op_graph.op.ReadFromParquet():
                return self._execute_read_from_parquet(op, context)
            case op_graph.op.RenameColumns():
                return self._execute_rename_columns(op, context)
            case op_graph.op.Join():
                return self._execute_join(op, context)
            case op_graph.op.SelectColumns():
                return self._execute_select_columns(op, context)
            case op_graph.op.LimitRows():
                return self._execute_limit_rows(op, context)
            case op_graph.op.OffsetRows():
                return self._execute_offset_rows(op, context)
            case op_graph.op.OrderBy():
                return self._execute_order_by(op, context)
            case op_graph.op.FilterRows():
                return self._execute_filter_rows(op, context)
            case op_graph.op.DistinctRows():
                return self._execute_distinct_rows(op, context)
            case (
                op_graph.op.SetMetadata()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
            ):
                return self._execute(op.source, context)
            case op_graph.op.EmbeddingMetrics() as op:
                return self._execute_embedding_metrics(op, context)
            case op_graph.op.EmbeddingCoordinates():
                return self._execute_embedding_coordinates(op, context)
            case op_graph.op.RollupByAggregation() as op:
                return self._execute_rollup_by_aggregation(op, context)
            case op_graph.op.Empty():
                return self._execute_empty(op, context)
            case op_graph.op.EmbedNode2vecFromEdgeLists():
                return self._execute_embed_node2vec_from_edge_lists(op, context)
            case op_graph.op.Concat():
                return self._execute_concat(op, context)
            case op_graph.op.UnnestStruct():
                return self._execute_unnest_struct(op, context)
            case op_graph.op.NestIntoStruct():
                return self._execute_nest_into_struct(op, context)
            case op_graph.op.AddLiteralColumn():
                return self._execute_add_literal_column(op, context)
            case op_graph.op.CombineColumns():
                return self._execute_combine_columns(op, context)
            case op_graph.op.EmbedColumn():
                return self._execute_embed_column(op, context)
            case op_graph.op.EncodeColumns():
                return self._execute_encode_columns(op, context)
            case op_graph.op.AggregateColumns():
                return self._execute_aggregate_columns(op, context)
            case op_graph.op.CorrelateColumns():
                return self._execute_correlate_columns(op, context)
            case op_graph.op.HistogramColumn():
                return self._execute_histogram_column(op, context)
            case op_graph.op.ConvertColumnToString():
                return self._execute_convert_column_to_string(op, context)
            case op_graph.op.AddRowIndex():
                return self._execute_add_row_index(op, context)
            case op_graph.op.OutputCsv():
                return self._execute_output_csv(op, context)
            case op_graph.op.TruncateList():
                return self._execute_truncate_list(op, context)
            case op_graph.op.Union():
                return self._execute_union(op, context)
            case op_graph.op.EmbedImageColumn():
                return self._execute_embed_image_column(op, context)
            case op_graph.op.AddDecisionTreeSummary():
                return self._execute_add_decision_tree_summary(op, context)
            case op_graph.op.UnnestList():
                return self._execute_unnest_list(op, context)
            case op_graph.op.SampleRows():
                return self._execute_sample_rows(op, context)
            case op_graph.op.DescribeColumns():
                return self._execute_describe_columns(op, context)

    def _execute(
        self,
        op: op_graph.Op,
        context: _InMemoryExecutionContext,
    ) -> (
        Ok[_LazyFrameWithMetrics]
        | InternalError
        | ResourceExhaustedError
        | InvalidArgumentError
    ):
        tracer = None
        kind = None
        try:
            from opentelemetry import trace
        except ImportError:
            pass
        else:
            tracer = trace.get_tracer("corvic")
            kind = trace.SpanKind.INTERNAL
        with (
            structlog.contextvars.bound_contextvars(
                executing_op=op.expected_oneof_field()
            ),
            tracer.start_as_current_span(
                op.expected_oneof_field(),
                kind=kind,
            )
            if tracer and kind
            else nullcontext() as span,
        ):
            sliced_table = _SlicedTable(op, context.current_slice_args)
            if sliced_table in context.computed_batches_for_op_graph:
                _logger.info("using previously computed table for op")
                return Ok(context.computed_batches_for_op_graph[sliced_table])

            try:
                _logger.info("starting op execution")
                maybe_lfm = self._do_execute(op=op, context=context)
            finally:
                _logger.info("op execution complete")
            match maybe_lfm:
                case Ok(lfm):
                    pass
                case err:
                    if span:
                        span.record_exception(exception=err)
                    return err

            if (
                sliced_table in context.output_tables
                or sliced_table in context.reused_tables
            ):
                # collect the lazy frame since it will be re-used to avoid
                # re-computation
                dataframe = lfm.data.collect()
                lfm = _LazyFrameWithMetrics(dataframe.lazy(), lfm.metrics)
                context.computed_batches_for_op_graph[sliced_table] = lfm
            return Ok(lfm)

    def execute(
        self, context: ExecutionContext
    ) -> (
        Ok[ExecutionResult]
        | InvalidArgumentError
        | InternalError
        | ResourceExhaustedError
    ):
        with _InMemoryExecutionContext(context) as in_memory_context:
            for table_context in context.tables_to_compute:
                in_memory_context.current_output_context = table_context
                sliced_table = _SlicedTable(
                    table_context.table_op_graph, table_context.sql_output_slice_args
                )
                if sliced_table not in in_memory_context.computed_batches_for_op_graph:
                    match self._execute(sliced_table.op_graph, in_memory_context):
                        case Ok():
                            pass
                        case err:
                            return err
        args_lfm_iterator = in_memory_context.computed_batches_for_op_graph.items()
        computed_tables = {
            slice_args: _SchemaAndBatches.from_lazy_frame_with_metrics(lfm)
            for slice_args, lfm in args_lfm_iterator
        }

        return Ok(
            InMemoryExecutionResult.make(
                self._storage_manager, computed_tables, context
            )
        )
