from __future__ import annotations

from pypika import functions as fn
from pypika.queries import QueryBuilder, Table

from tesseract_olap.common import shorthash
from tesseract_olap.schema import CubeTraverser, models

from .backend import ParamManager
from .dialect import ClickhouseJoin, ClickhouseJoinType, ClickHouseQuery, TypedDictCursor


def extract_member_count(cube: CubeTraverser, cursor: TypedDictCursor) -> dict[str, int]:
    query, meta = sql_cubemembers(cube)

    cursor.reset_cursor()
    for table in meta.tables:
        cursor.set_inline_table(table)
    cursor.execute(query.get_sql())

    result: dict[str, int] = cursor.fetchone() or {"_empty": 0}
    return result


def sql_cubemembers(cube: CubeTraverser) -> tuple[QueryBuilder, ParamManager]:
    fact_table = Table(cube.table.name, alias="tfact")
    query = ClickHouseQuery._builder()
    meta = ParamManager()
    flag_join = False

    for dimension in cube.dimensions:
        for hierarchy in dimension.hierarchies:
            table = hierarchy.table
            table_alias = shorthash(f"{dimension.name}.{hierarchy.name}")
            levels = [(level, shorthash(level.name)) for level in hierarchy.levels]

            if table is None:
                gen_columns = (
                    fn.Count(fact_table.field(level.key_column), alias).distinct()
                    for level, alias in levels
                )
                tquery = (
                    ClickHouseQuery.from_(fact_table).select(*gen_columns).as_(f"sq_{table_alias}")
                )

            else:
                if isinstance(table, models.InlineTable):
                    meta.set_table(table)

                dim_table = Table(table.name, alias="tdim")

                gen_columns = (
                    fn.Count(dim_table.field(level.key_column), alias).distinct()
                    for level, alias in levels
                )
                tquery = (
                    ClickHouseQuery.from_(dim_table)
                    .select(*gen_columns)
                    .where(
                        dim_table.field(hierarchy.primary_key).isin(
                            ClickHouseQuery.from_(fact_table)
                            .select(fact_table.field(dimension.foreign_key))
                            .distinct(),
                        ),
                    )
                    .as_(f"sq_{table_alias}")
                )

            if flag_join:
                query.do_join(ClickhouseJoin(tquery, ClickhouseJoinType.paste))
            else:
                query = query.from_(tquery)
                flag_join = True

            gen_fields = (tquery.field(alias).as_(level.name) for level, alias in levels)
            query = query.select(*gen_fields)

    return query, meta
