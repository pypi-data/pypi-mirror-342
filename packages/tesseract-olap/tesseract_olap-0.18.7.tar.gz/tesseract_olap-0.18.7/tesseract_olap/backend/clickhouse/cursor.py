import logging
from collections import defaultdict

from tesseract_olap.exceptions.backend import BackendValidationError
from tesseract_olap.schema import InlineTable, Measure, SchemaTraverser

from .dialect import TypedCursor, TypedDictCursor
from .sql_members import extract_member_count

logger = logging.getLogger(__name__)


def count_members(schema: SchemaTraverser, cursor: TypedDictCursor) -> None:
    """Query the backend for an updated number of members of each Level."""
    count_total = sum(
        len(hie.level_map)
        for cube in schema.cube_map.values()
        for dim in cube.dimensions
        for hie in dim.hierarchies
    )
    count_progress = 0

    for cube in sorted(schema.cube_map.values(), key=lambda cube: cube.name):
        members = extract_member_count(cube, cursor)
        count_progress += len(members)

        for level in cube.levels:
            level.count = members.get(level.name, 0)
            if level.count == 0:
                logger.warning(
                    "Level(cube=%r, name=%r) returned 0 members",
                    cube.name,
                    level.name,
                )

        args = (cube.name, count_progress, count_total)
        logger.debug("Updated member count for cube %r (%d/%d)", *args, extra=members)


def validate_schema_tables(schema: "SchemaTraverser", cursor: "TypedCursor") -> None:
    """Validate the tables and columns declared in the Schema entities against the Backend."""
    schema_tables = unwrap_tables(schema)
    logger.debug("Tables to validate: %d", len(schema_tables))

    sql = (
        "SELECT table, groupArray(name) AS columns "
        "FROM system.columns "
        "WHERE table IN splitByChar(',', %(tables)s) "
        "GROUP BY table"
    )
    cursor.execute(sql, {"tables": ",".join(schema_tables.keys())})
    observed_tables = {table: set(columns) for table, columns in (cursor.fetchall() or [])}

    if schema_tables != observed_tables:
        reasons = []

        for table, columns in schema_tables.items():
            if table not in observed_tables:
                reasons.append(
                    f"- Table '{table}' is defined in Schema but not available in Backend",
                )
                continue

            difference = columns.difference(observed_tables[table])
            if difference:
                reasons.append(
                    f"- Schema references columns {difference} in table '{table}', but not available in Backend",
                )

        if reasons:
            message = (
                "Mismatch between columns defined in the Schema and available in ClickhouseBackend:\n"
                + "\n".join(reasons)
            )
            raise BackendValidationError(message)


def unwrap_tables(self: SchemaTraverser) -> dict[str, set[str]]:
    """Extract the {table: column[]} data from all entities in the schema."""
    tables: dict[str, set[str]] = defaultdict(set)

    for cube in self.cube_map.values():
        table = cube.table
        if isinstance(table, InlineTable):
            continue

        # Index fact tables
        tables[table.name].update(
            (
                item.key_column
                for measure in cube.measures
                for item in measure.and_submeasures()
                if isinstance(item, Measure)
            ),
            (dimension.foreign_key for dimension in cube.dimensions),
        )

        for hierarchy in cube.hierarchies:
            table = hierarchy.table
            if table is None or isinstance(table, InlineTable):
                continue

            # Index dimension tables
            tables[table.name].update(
                (
                    item
                    for level in hierarchy.levels
                    for item in (level.key_column, *level.name_column_map.values())
                ),
                (
                    item
                    for propty in hierarchy.properties
                    for item in propty.key_column_map.values()
                ),
            )

    return dict(tables)
