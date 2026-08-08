from services.schema_service import load_schema


def build_mini_schema(

    selected_tables,

    selected_columns

):

    """
    selected_tables:
    [
        {"table":"keluarga",...},
        ...
    ]

    selected_columns:
    [
        {"table":"keluarga","column":"nama"},
        ...
    ]
    """

    schema = load_schema()

    if schema is None:

        raise Exception(

            "Schema belum tersedia."

        )

    table_set = {

        t["table"]

        for t in selected_tables

    }

    column_map = {}

    for column in selected_columns:

        table = column["table"]

        if table not in column_map:

            column_map[table] = set()

        column_map[table].add(

            column["column"]

        )

    mini_tables = []

    for table in schema["tables"]:

        if table["table"] not in table_set:

            continue

        new_table = table.copy()

        new_columns = []

        for column in table["columns"]:

            if column["name"] in column_map.get(

                table["table"],

                set()

            ):

                new_columns.append(

                    column

                )

        new_table["columns"] = new_columns

        mini_tables.append(

            new_table

        )

    return {

        "database":

            schema["database"],

        "description":

            schema.get(

                "description",

                ""

            ),

        "tables":

            mini_tables

    }