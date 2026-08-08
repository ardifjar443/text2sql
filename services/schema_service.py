from pathlib import Path
import json
from datetime import datetime
import shutil

from services.embedding_service import clear_current_embedding


SCHEMA_DIR = Path("data/schema")

SCHEMA_DIR.mkdir(
    exist_ok=True
)

SCHEMA_PATH = SCHEMA_DIR / "schema_metadata.json"

SCHEMA_METADATA_FILE = SCHEMA_DIR / "metadata.json"


def load_schema():

    if not SCHEMA_PATH.exists():

        return None

    with open(

        SCHEMA_PATH,

        encoding="utf8"

    ) as f:

        return json.load(f)


def save_schema(file):

    file.save(SCHEMA_PATH)

    with open(
        SCHEMA_PATH,
        encoding="utf8"
    ) as f:

        schema = json.load(f)

    metadata = create_metadata(schema)

    with open(
        SCHEMA_METADATA_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )

    clear_current_embedding()




def schema_summary():

    schema = load_schema()

    if schema is None:

        return {

            "tables":0,

            "columns":0,

            "relationships":0

        }

    table_count = len(

        schema["tables"]

    )

    column_count = 0

    relationship_count = 0

    for table in schema["tables"]:

        column_count += len(

            table["columns"]

        )

        relationship_count += len(

            table.get(

                "foreign_keys",

                []

            )

        )

    return {

        "tables":table_count,

        "columns":column_count,

        "relationships":relationship_count

    }
    




def create_metadata(schema):

    total_tables = len(schema["tables"])

    total_columns = sum(

        len(t["columns"])

        for t in schema["tables"]

    )

    total_relationships = sum(

        len(

            t.get(

                "foreign_keys",

                []

            )

        )

        for t in schema["tables"]

    )

    return {

        "database":

            schema.get(

                "database",

                "Unknown"

            ),

        "description":

            schema.get(

                "description",

                "-"

            ),

        "version":

            schema.get(

                "version",

                "1.0"

            ),

        "created_at":

            datetime.now()

            .strftime(

                "%Y-%m-%d %H:%M:%S"

            ),

        "table_count":

            total_tables,

        "column_count":

            total_columns,

        "relationship_count":

            total_relationships,

        "schema_file":

            SCHEMA_PATH.name

    }
    
def get_current_database():

    if not SCHEMA_METADATA_FILE.exists():

        return None

    with open(

        SCHEMA_METADATA_FILE,

        encoding="utf8"

    ) as f:

        return json.load(f)
    
    
# ==========================================================
# BUILD FULL SCHEMA
# ==========================================================

def build_full_schema():

    schema = load_schema()

    if schema is None:

        return {}

    result = {}

    for table in schema["tables"]:

        result[table["table"]] = {

            "description": table.get(
                "description",
                ""
            ),

            "primary_key": table.get(
                "primary_key",
                ""
            ),

            "foreign_keys": table.get(
                "foreign_keys",
                []
            ),

            "columns": table["columns"]

        }

    return result


# ==========================================================
# BUILD MINI SCHEMA
# ==========================================================

def build_mini_schema(

    selected_tables,

    selected_columns

):

    schema = {}

    for table in selected_tables:

        schema[table["table"]] = {

            "description":

                table.get(
                    "description",
                    ""
                ),

            "primary_key":

                table.get(
                    "primary_key",
                    ""
                ),

            "foreign_keys":

                table.get(
                    "foreign_keys",
                    []
                ),

            "columns": []

        }

    for column in selected_columns:

        table_name = column["table"]

        if table_name not in schema:

            continue

        schema[table_name]["columns"].append({

            "name":

                column["column"],

            "type":

                column["type"],

            "description":

                column["description"]

        })

    return schema