# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pyarrow as pa
from lancedb.query import LanceEmptyQueryBuilder, Query
from lancedb.rerankers.base import Reranker
from numpy.random import default_rng
from pydantic import BaseModel

# Self / override is not available in python 3.10
from typing_extensions import Self, override  # noqa: UP035

from geneva.db import Connection
from geneva.packager import UDFPackager, UDFSpec
from geneva.transformer import UDF

if TYPE_CHECKING:
    from lance import LanceDataset

    from geneva.table import Table


MATVIEW_META = "geneva::view::"
MATVIEW_META_QUERY = f"{MATVIEW_META}query"
MATVIEW_META_BASE_TABLE = f"{MATVIEW_META}base_table"
MATVIEW_META_BASE_DBURI = f"{MATVIEW_META}base_table_db_uri"
MATVIEW_META_BASE_VERSION = f"{MATVIEW_META}base_table_version"


class PydanticUDFSpec(BaseModel):
    name: str
    backend: str
    udf_payload: bytes
    runner_payload: bytes | None

    @classmethod
    def from_attrs(cls, spec: UDFSpec) -> "PydanticUDFSpec":
        return PydanticUDFSpec(
            name=spec.name,
            backend=spec.backend,
            udf_payload=spec.udf_payload,
            runner_payload=spec.runner_payload,
        )

    def to_attrs(self) -> UDFSpec:
        return UDFSpec(
            name=self.name,
            backend=self.backend,
            udf_payload=self.udf_payload,
            runner_payload=self.runner_payload,
        )


class ColumnUDF(BaseModel):
    output_index: int
    output_name: str
    udf: PydanticUDFSpec


@dataclass
class ExtractedTransform:
    output_index: int
    output_name: str
    udf: UDF


class GenevaQuery(BaseModel):
    base: Query
    shuffle: bool | None = None
    shuffle_seed: int | None = None
    fragment_ids: list[int] | None = None
    with_row_address: bool | None = None
    column_udfs: list[ColumnUDF] | None = None

    def extract_column_udfs(self, packager: UDFPackager) -> list[ExtractedTransform]:
        """
        Loads a set of transforms that reflect the column_udfs and map_batches_udfs
        of the query.
        """
        transforms = []
        if self.column_udfs is not None:
            for column_udf in self.column_udfs:
                udf = packager.unmarshal(column_udf.udf.to_attrs())
                transforms.append(
                    ExtractedTransform(
                        output_index=column_udf.output_index,
                        output_name=column_udf.output_name,
                        udf=udf,
                    )
                )
        return transforms


class GenevaQueryBuilder(LanceEmptyQueryBuilder):
    """A proxy that wraps LanceQueryBuilder and adds geneva-specific functionality."""

    def __init__(self, table: "Table") -> None:
        super().__init__(table)
        self._table = table
        self._shuffle = None
        self._shuffle_seed = None
        self._fragment_ids = None
        self._with_row_address = None
        self._internal_api_enabled = False
        self._column_udfs = None

    def _internal_api_only(self) -> None:
        if not self._internal_api_enabled:
            raise ValueError(
                "This method is for internal use only and subject to change. "
                "Call enable_internal_api() first to enable."
            )

    @override
    def select(self, columns: list[str] | dict[str, str | UDF]) -> Self:
        """
        Select the output columns of the query.

        Parameters
        ----------
        columns: list[str] | dict[str, str] | dict[str, UDF]
            The columns to select.

            If a list of strings, each string is the name of a column to select.

            If a dictionary of strings then the key is the output name of the column
            and the value is either an SQL expression (str) or a UDF.
        """
        if isinstance(columns, dict):
            self._column_udfs = {
                key: (value, index)
                for (index, (key, value)) in enumerate(columns.items())
                if isinstance(value, UDF)
            }
            columns = {
                key: value
                for key, value in columns.items()
                if not isinstance(value, UDF)
            }

        super().select(columns)
        return self

    def shuffle(self, seed: int | None = None) -> Self:
        """Shuffle the rows of the table"""
        self._shuffle = True
        self._shuffle_seed = seed
        return self

    def enable_internal_api(self) -> Self:
        """
        Enable internal APIs
        WARNING: Internal APIs are subject to change
        """
        self._internal_api_enabled = True
        return self

    def with_fragments(self, fragments: list[int] | int) -> Self:
        """
        Filter the rows of the table to only include the specified fragments.
        """
        self._internal_api_only()
        self._fragment_ids = [fragments] if isinstance(fragments, int) else fragments
        return self

    def with_row_address(self) -> Self:
        """
        Include the physical row address in the result
        WARNING: INTERNAL API DETAIL
        """
        self._internal_api_only()
        self._with_row_address = True
        return self

    @override
    def to_query_object(self) -> GenevaQuery:  # type: ignore
        query = super().to_query_object()
        result = GenevaQuery(
            base=query,
            shuffle=self._shuffle,
            shuffle_seed=self._shuffle_seed,
            fragment_ids=self._fragment_ids,
            with_row_address=self._with_row_address,
        )
        if self._column_udfs:
            result.column_udfs = [
                ColumnUDF(
                    output_index=index,
                    output_name=name,
                    udf=PydanticUDFSpec.from_attrs(
                        self._table._conn._packager.marshal(udf)
                    ),
                )
                for (name, (udf, index)) in self._column_udfs.items()
            ]
        return result

    @classmethod
    def from_query_object(
        cls, table: "Table", query: GenevaQuery
    ) -> "GenevaQueryBuilder":
        result = GenevaQueryBuilder(table)

        # TODO: Add from_query_object to lancedb.  For now, this will work
        # for simple (non-vector, non-fts) queries.
        if query.base.columns is not None:
            result.select(query.base.columns)
        if query.base.filter:
            result.where(query.base.filter)
        if query.base.limit:
            result.limit(query.base.limit)
        if query.base.offset:
            result.offset(query.base.offset)
        if query.base.with_row_id:
            result.with_row_id(True)

        result._shuffle = query.shuffle
        result._shuffle_seed = query.shuffle_seed
        if query.column_udfs:
            result._column_udfs = {}
            for column_udf in query.column_udfs:
                udf = table._conn._packager.unmarshal(column_udf.udf.to_attrs())
                result._column_udfs[column_udf.output_name] = (
                    udf,
                    column_udf.output_index,
                )
        result._fragment_ids = query.fragment_ids
        result._with_row_address = query.with_row_address
        result._internal_api_enabled = True
        return result

    def take_rows(self, rows: list[int]) -> pa.Table:
        query = self.to_query_object()
        return self._table.to_lance()._take_rows(rows, query.base.columns)

    def _schema_for_query(self, include_metacols: bool = True) -> pa.Schema:
        schema = self._table.schema

        base_query = super().to_query_object()

        if base_query.columns is not None:
            if isinstance(base_query.columns, list):
                fields = [schema.field(col) for col in base_query.columns]
            else:
                fields = []
                for dest_name, expr in base_query.columns.items():
                    try:
                        field = schema.field(expr)
                    except KeyError as e:
                        # TODO: Need to get output type from SQL expression
                        raise NotImplementedError(
                            f"SQL expression {expr} not yet supported"
                        ) from e
                    fields.append(pa.field(dest_name, field.type, field.nullable))

        else:
            fields = list(schema)

        if self._column_udfs is not None:
            for output_name, (udf, output_index) in self._column_udfs.items():
                fields.insert(output_index, pa.field(output_name, udf.data_type))

        if include_metacols and base_query.with_row_id:
            fields += [pa.field("_rowid", pa.int64())]

        if include_metacols and self._with_row_address:
            fields += [pa.field("_rowaddr", pa.int64())]

        return pa.schema(fields)

    @property
    def schema(self) -> pa.Schema:
        return self._schema_for_query()

    @override
    def to_batches(self, /, batch_size: int | None = None) -> pa.RecordBatchReader:
        schema = self._schema_for_query(include_metacols=False)
        blob_columns = {}
        for field_idx, field in enumerate(schema):
            if field.metadata and field.metadata.get(b"lance-encoding:blob") == b"true":
                blob_columns[field.name] = field_idx

        base_query = super().to_query_object()
        if len(blob_columns) > 0:
            base_query.with_row_id = True

        if self._shuffle:
            raise NotImplementedError("Shuffle is not yet implemented")

        dataset: LanceDataset = self._table.to_lance()

        fragments = None
        if self._fragment_ids:
            fragments = [dataset.get_fragment(fid) for fid in self._fragment_ids]

        if base_query.vector:
            raise NotImplementedError("vector search not yet implemented")

        if base_query.full_text_query:
            raise NotImplementedError("fts search not yet implemented")

        # If we have UDFs, and the user isn't grabbing ALL columns from the base
        # query, we might need to grab additional columns to satisfy the UDFs.
        extra_columns = []
        if (
            self._column_udfs is not None
            and len(self._column_udfs) > 0
            and base_query.columns is not None
        ):
            if isinstance(base_query.columns, list):
                potential_udf_inputs = set(base_query.columns)
            else:
                potential_udf_inputs = set(base_query.columns.keys())

            for udf, _ in self._column_udfs.values():
                if udf.input_columns is None:
                    continue
                for input_col in udf.input_columns:
                    if input_col not in potential_udf_inputs:
                        extra_columns.append(input_col)
                        potential_udf_inputs.add(input_col)

        # Add the extra columns to the columns we are grabbing and record the
        # position so we can remove them later.
        added_columns = []
        if base_query.columns is not None:
            if isinstance(base_query.columns, list):
                for extra_column in extra_columns:
                    added_columns.append(len(base_query.columns))
                    base_query.columns.append(extra_column)
            else:
                for extra_column in extra_columns:
                    added_columns.append(len(base_query.columns))
                    base_query.columns[extra_column] = extra_column

        batch_gen = dataset.scanner(
            columns=base_query.columns,
            with_row_id=base_query.with_row_id,
            with_row_address=self._with_row_address,
            filter=base_query.filter,
            batch_size=batch_size,
            offset=base_query.offset,
            limit=base_query.limit,
            fragments=fragments,
        ).to_batches()

        schema = self._schema_for_query(include_metacols=True)

        def map_columns() -> Iterator[pa.RecordBatch]:
            for batch in batch_gen:
                if blob_columns:
                    for blob_column_idx, blob_column in blob_columns.items():
                        files = dataset.take_blobs(
                            batch["_rowid"],
                            blob_column,
                        )
                        batch = batch.set_column(blob_column_idx, files)

                if self._column_udfs:
                    for col_name, (udf, index) in self._column_udfs.items():
                        arr = udf(batch)
                        batch = batch.add_column(
                            index, pa.field(col_name, arr.type), arr
                        )

                    # Remove any columns that were fetched just for the purposes
                    # of being used as UDF inputs
                    for added_idx in reversed(added_columns):
                        batch = batch.remove_column(added_idx + len(self._column_udfs))

                yield batch

        return pa.RecordBatchReader.from_batches(schema, map_columns())

    @override
    def to_arrow(self) -> pa.Table:
        return pa.Table.from_batches(self.to_batches())

    @override
    def rerank(self, reranker: Reranker) -> Self:
        raise NotImplementedError("rerank is not yet implemented")

    def create_materialized_view(self, conn: Connection, view_name: str) -> "Table":
        """
        Creates a materialized view of the table.

        The materialized view will be a table that contains the result of the query.
        The view will be populated via a pipeline job.

        Parameters
        ----------
        conn: Connection
            A connection to the database to create the view in.
        view_name: str
            The name of the view to create.
        """
        view_schema = self._schema_for_query(include_metacols=True)
        view_schema = view_schema.insert(0, pa.field("__is_set", pa.bool_()))
        view_schema = view_schema.insert(0, pa.field("__source_row_id", pa.int64()))

        query = self.to_query_object()
        view_schema = view_schema.with_metadata(
            {
                MATVIEW_META_QUERY: query.model_dump_json(),
                MATVIEW_META_BASE_TABLE: self._table._ltbl.name,
                MATVIEW_META_BASE_DBURI: self._table._conn_uri,
                MATVIEW_META_BASE_VERSION: str(self._table._ltbl.version),
                # TODO: Add the base DB URI (should be possible
                # to get from lancedb table in future)
            }
        )

        row_ids_query = GenevaQuery(
            fragment_ids=query.fragment_ids,
            base=query.base,
        )
        row_ids_query.base.with_row_id = True
        row_ids_query.base.columns = []
        row_ids_query.column_udfs = None
        row_ids_query.with_row_address = None

        row_ids_query_builder = GenevaQueryBuilder.from_query_object(
            self._table, row_ids_query
        )

        row_ids_table = row_ids_query_builder.to_arrow()
        row_ids_table = row_ids_table.combine_chunks()
        # Copy is needed so that the array is not read-only
        row_ids = row_ids_table["_rowid"].to_numpy().copy()

        if query.shuffle:
            rng = default_rng(query.shuffle_seed)
            rng.shuffle(row_ids)

        initial_view_table_data = pa.table(
            {
                "__source_row_id": row_ids,
                "__is_set": pa.array([False] * len(row_ids)),
            }
        )

        # Need to create table in two steps because partial schema is not allowed
        # on initial create_table call.
        view_table = conn.create_table(
            view_name, data=None, schema=view_schema, mode="create"
        )
        view_table.add(initial_view_table_data)
        return view_table


class Column:
    """Present a Column in the Table."""

    def __init__(self, name: str) -> None:
        """Define a column."""
        self.name = name

    def alias(self, alias: str) -> "Column":
        return AliasColumn(self, alias)

    def blob(self) -> "Column":
        return BlobColumn(self)

    def apply(self, batch: pa.RecordBatch) -> tuple[str, pa.Array]:
        return (self.name, batch[self.name])


class BlobColumn(Column):
    def __init__(self, col: Column) -> None:
        self.inner = col


class AliasColumn(Column):
    def __init__(self, col: Column, alias: str) -> None:
        self.col = col
        self._alias = alias

    def apply(self, batch: pa.RecordBatch) -> tuple[str, pa.Array]:
        _, arr = self.col.apply(batch)
        return (self._alias, arr)
