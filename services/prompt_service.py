from datetime import datetime


# ==========================================================
# PROMPT VERSION
# ==========================================================

PROMPT_VERSION = "v1.0"


# ==========================================================
# SYSTEM ROLE
# ==========================================================

SYSTEM_ROLE = """
You are an expert MySQL Text-to-SQL model.

Your task is converting natural language questions into
correct MySQL SQL queries.

Return ONLY SQL.

Never explain.

Never generate markdown.

Never generate comments.
""".strip()


# ==========================================================
# DATABASE CONTEXT
# ==========================================================

DATABASE_CONTEXT = """
Database Name:
{database}

Description:
{description}

This database contains Indonesian social welfare data.

The schema supplied below is the ONLY source of truth.

Never use tables or columns outside the supplied schema.
""".strip()


# ==========================================================
# RULES
# ==========================================================

RULES = [

    "Generate exactly ONE SQL query.",

    "Use MySQL syntax.",

    "Return SQL only.",

    "Never explain the answer.",

    "Never generate markdown.",

    "Never create tables or columns that do not exist.",

    "Only use the supplied schema.",

    "Use JOIN only when necessary.",

    "Use aggregate functions correctly.",

    "Use aliases when improving readability.",

    "Do not retrieve sensitive information unless explicitly requested."

]


# ==========================================================
# PROMPT MODE
# ==========================================================

PROMPT_MODE = {

    "full_schema": "Full Schema",

    "retrieval": "Retrieved Schema"

}

from pathlib import Path
import json
import shutil
from datetime import datetime

PROMPT_DIR = Path("data/prompt")

CURRENT_DIR = PROMPT_DIR / "current"

HISTORY_DIR = PROMPT_DIR / "history"

CURRENT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

PROMPT_FILE = CURRENT_DIR / "prompt.txt"

METADATA_FILE = CURRENT_DIR / "metadata.json"


# ==========================================================
# BUILD RULES
# ==========================================================

def build_rules():

    text = ""

    for i, rule in enumerate(

        RULES,

        start=1

    ):

        text += f"{i}. {rule}\n"

    return text.strip()


# ==========================================================
# BUILD DATABASE CONTEXT
# ==========================================================

def build_database_context(

    metadata

):

    return DATABASE_CONTEXT.format(

        database=metadata.get(

            "database",

            "Unknown"

        ),

        description=metadata.get(

            "description",

            "-"

        )

    )


# ==========================================================
# BUILD SCHEMA
# ==========================================================

def build_schema(schema):

    if not schema:
        return "Schema not available."

    text = ""

    for table in schema["tables"]:

        text += "=" * 60 + "\n"

        # ==========================================
        # TABLE
        # ==========================================

        text += f"TABLE : {table['table']}\n"

        text += (
            f"DESCRIPTION : "
            f"{table.get('description', '')}\n"
        )

        # ==========================================
        # PRIMARY KEY
        # ==========================================

        primary_keys = table.get(
            "primary_key",
            []
        )

        # PK bisa berupa string atau list
        if isinstance(primary_keys, str):
            primary_keys = [primary_keys]

        if primary_keys is None:
            primary_keys = []

        text += "\n"

        if primary_keys:
            text += "PRIMARY KEY : "
            text += ", ".join(primary_keys)
            text += "\n"

        # ==========================================
        # COLUMNS
        # ==========================================

        text += "\n"
        text += "COLUMNS\n"

        # ==========================================
        # FOREIGN KEYS
        # ==========================================

        foreign_keys = table.get(
            "foreign_keys",
            []
        )

        if foreign_keys is None:
            foreign_keys = []

        # Buat mapping FK berdasarkan nama column
        foreign_key_map = {
            fk["column"]: fk.get(
                "references",
                ""
            )
            for fk in foreign_keys
            if "column" in fk
        }

        # ==========================================
        # COLUMN LOOP
        # ==========================================

        for column in table["columns"]:

            column_name = column["name"]

            column_type = column["type"]

            description = column.get(
                "description",
                ""
            )

            # --------------------------------------
            # COLUMN ROLE
            # --------------------------------------

            is_primary_key = (
                column_name in primary_keys
            )

            is_foreign_key = (
                column_name in foreign_key_map
            )

            # --------------------------------------
            # BASIC COLUMN
            # --------------------------------------

            text += (
                f"- {column_name} "
                f"({column_type}) "
                f": {description}"
            )

            # --------------------------------------
            # PRIMARY KEY LABEL
            # --------------------------------------

            if is_primary_key:

                text += " [PRIMARY KEY]"

            # --------------------------------------
            # FOREIGN KEY LABEL
            # --------------------------------------

            if is_foreign_key:

                text += (
                    f" [FOREIGN KEY -> "
                    f"{foreign_key_map[column_name]}]"
                )

            text += "\n"

        # ==========================================
        # FOREIGN KEYS SECTION
        # ==========================================

        if foreign_keys:

            text += "\n"
            text += "FOREIGN KEYS\n"

            for fk in foreign_keys:

                text += (
                    f"- {fk['column']} "
                    f"-> "
                    f"{fk['references']}\n"
                )

        text += "\n"

    return text.strip()

# ==========================================================
# BUILD QUESTION
# ==========================================================

def build_question(

    question

):

    return f"QUESTION:\n{question}"


# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_prompt(

    metadata,

    schema,

    question

):

    prompt = ""

    prompt += "# ROLE\n\n"

    prompt += SYSTEM_ROLE

    prompt += "\n\n"

    prompt += "# DATABASE\n\n"

    prompt += build_database_context(

        metadata

    )

    prompt += "\n\n"

    prompt += "# SCHEMA\n\n"

    prompt += build_schema(

        schema

    )

    prompt += "\n\n"

    prompt += "# RULES\n\n"

    prompt += build_rules()

    prompt += "\n\n"

    prompt += build_question(

        question

    )

    prompt += "\n\nSQL:\n"

    return prompt


# ==========================================================
# PROMPT METADATA
# ==========================================================

def prompt_metadata():

    return {

        "version": PROMPT_VERSION,

        "created_at": datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        ),

        "total_rules": len(RULES)

    }
    
# ==========================================================
# PROMPT VERSION LIST
# ==========================================================

PROMPT_VERSIONS = {

    "v1": {

        "name": "Default Prompt",

        "description": "Standard Text-to-SQL Prompt"

    },

    "v2": {

        "name": "Prompt With Few Shot",

        "description": "Prompt + Example SQL"

    }

}


def get_prompt_versions():

    return PROMPT_VERSIONS

# ==========================================================
# FEW SHOT EXAMPLES
# ==========================================================

FEW_SHOT = [

    {

        "question":

        "Berapa jumlah keluarga?",

        "sql":

        "SELECT COUNT(*) FROM keluarga;"

    },

    {

        "question":

        "Berapa jumlah anggota keluarga?",

        "sql":

        "SELECT COUNT(*) FROM anggota_keluarga;"

    }

]


# ==========================================================
# BUILD FEW SHOT
# ==========================================================

def build_few_shot():

    text = ""

    for example in FEW_SHOT:

        text += "Question:\n"

        text += example["question"]

        text += "\n\n"

        text += "SQL:\n"

        text += example["sql"]

        text += "\n\n"

    return text.strip()

# ==========================================================
# PROMPT STATISTICS
# ==========================================================

def prompt_statistics(

    prompt,

    schema

):

    table_count = len(

        schema["tables"]

    )

    column_count = sum(

        len(t["columns"])

        for t in schema["tables"]

    )

    return {

        "characters":

            len(prompt),

        "words":

            len(

                prompt.split()

            ),

        "tables":

            table_count,

        "columns":

            column_count

    }
    
    
# ==========================================================
# BUILD PROMPT V2
# ==========================================================

def build_prompt_v2(

    metadata,

    schema,

    question,

    use_example=False

):

    prompt = build_prompt(

        metadata,

        schema,

        question

    )

    if use_example:

        prompt += "\n\n"

        prompt += "# EXAMPLES\n\n"

        prompt += build_few_shot()

    return prompt

# ==========================================================
# PROMPT INFO
# ==========================================================

def get_prompt_information(

    metadata,

    schema,

    question,

    use_example=False

):

    prompt = build_prompt_v2(

        metadata,

        schema,

        question,

        use_example

    )

    stats = prompt_statistics(

        prompt,

        schema

    )

    return {

        "version":

            PROMPT_VERSION,

        "mode":

            "Full Schema",

        "statistics":

            stats,

        "prompt":

            prompt

    }
    
    
# ==========================================================
# RETRIEVAL MODE
# ==========================================================

RETRIEVAL_MODE = {

    "none": "Full Schema",

    "top1": "Top 1",

    "top3": "Top 3",

    "top5": "Top 5",

    "adaptive_gap": "Adaptive Gap",

    "adaptive_mean": "Adaptive Mean",

    "adaptive_mean_sd1": "Adaptive Mean SD",

    "adaptive_percentile75": "Adaptive Percentile"

}


def get_retrieval_modes():

    return RETRIEVAL_MODE

# ==========================================================
# SELECT SCHEMA
# ==========================================================

def select_schema(

    full_schema,

    retrieved_schema,

    retrieval_mode

):

    if retrieval_mode == "none":

        return full_schema

    return retrieved_schema


# ==========================================================
# PROMPT CONFIG
# ==========================================================

DEFAULT_PROMPT_CONFIG = {

    "version": "v1",

    "retrieval": "none",

    "few_shot": False,

    "temperature": 0,

    "top_p": 1,

    "max_tokens": 2048

}

# ==========================================================
# BUILD CONFIG
# ==========================================================

def build_prompt_config(

    **kwargs

):

    config = DEFAULT_PROMPT_CONFIG.copy()

    config.update(kwargs)

    return config

# ==========================================================
# PROMPT FACTORY
# ==========================================================

def build_experiment_prompt(

    metadata,

    full_schema,

    retrieved_schema,

    question,

    config

):

    schema = select_schema(

        full_schema,

        retrieved_schema,

        config["retrieval"]

    )

    prompt = build_prompt_v2(

        metadata,

        schema,

        question,

        config["few_shot"]

    )

    return {

        "prompt": prompt,

        "schema": schema,

        "config": config,

        "statistics":

            prompt_statistics(

                prompt,

                schema

            )

    }
    
# ==========================================================
# PROMPT PREVIEW
# ==========================================================

def preview_prompt(

    metadata,

    schema,

    question

):

    prompt = build_prompt(

        metadata,

        schema,

        question

    )

    return prompt[:3000]

# ==========================================================
# PROMPT SUMMARY
# ==========================================================

def prompt_summary(

    config,

    statistics

):

    return {

        "Prompt Version":

            config["version"],

        "Retrieval":

            config["retrieval"],

        "Few Shot":

            config["few_shot"],

        "Temperature":

            config["temperature"],

        "Top P":

            config["top_p"],

        "Max Tokens":

            config["max_tokens"],

        "Characters":

            statistics["characters"],

        "Words":

            statistics["words"],

        "Tables":

            statistics["tables"],

        "Columns":

            statistics["columns"]

    }
    
def load_prompt():

    if not PROMPT_FILE.exists():
        return ""

    with open(
        PROMPT_FILE,
        encoding="utf8"
    ) as f:

        return normalize_prompt(f.read())

def normalize_prompt(prompt):

    # ubah CRLF menjadi LF
    prompt = prompt.replace("\r\n", "\n")

    # hapus spasi/tab di setiap baris
    lines = [line.strip() for line in prompt.split("\n")]

    cleaned = []
    previous_blank = False

    for line in lines:

        if line == "":
            if not previous_blank:
                cleaned.append("")
            previous_blank = True
        else:
            cleaned.append(line)
            previous_blank = False

    return "\n".join(cleaned).strip()
    
def save_prompt(prompt_text):

    prompt_text = normalize_prompt(prompt_text)

    version = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    with open(
        PROMPT_FILE,
        "w",
        encoding="utf8"
    ) as f:

        f.write(prompt_text)

    metadata = {

        "version": version,

        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "characters": len(prompt_text),

        "words": len(prompt_text.split())

    }

    with open(
        METADATA_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )

    version_dir = HISTORY_DIR / version

    version_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        PROMPT_FILE,
        version_dir / "prompt.txt"
    )

    shutil.copy2(
        METADATA_FILE,
        version_dir / "metadata.json"
    )

def get_prompt_metadata():

    if not METADATA_FILE.exists():

        return None

    with open(

        METADATA_FILE,

        encoding="utf8"

    ) as f:

        return json.load(f)
    
def get_prompt_history():

    histories = []

    if not HISTORY_DIR.exists():

        return histories

    for folder in sorted(

        HISTORY_DIR.iterdir(),

        reverse=True

    ):

        meta = folder / "metadata.json"

        if meta.exists():

            with open(

                meta,

                encoding="utf8"

            ) as f:

                data = json.load(f)

            histories.append(data)

    return histories

from services.schema_service import load_schema
from services.schema_service import get_current_database


def schema_to_text(schema):
    """
    Mengubah JSON schema menjadi teks yang akan dimasukkan
    ke dalam prompt.

    Aturan:
    - Primary Key selalu ditampilkan
    - Foreign Key selalu ditampilkan
    - Semua kolom yang sudah dipilih oleh build_mini_schema
      tetap ditampilkan
    """

    if not schema:
        return "Schema not found."

    result = []

    database = schema.get(
        "database",
        "-"
    )

    result.append(
        f"Database : {database}\n"
    )

    for table in schema["tables"]:

        result.append(
            "=" * 60
        )

        result.append(
            f"TABLE : {table['table']}"
        )

        # ==========================================
        # TABLE DESCRIPTION
        # ==========================================

        if table.get("description"):

            result.append(
                f"Description : "
                f"{table['description']}"
            )

        # ==========================================
        # PRIMARY KEY
        # ==========================================

        primary_keys = table.get(
            "primary_key",
            []
        )

        # PK dapat berupa string atau list
        if isinstance(
            primary_keys,
            str
        ):
            primary_keys = [
                primary_keys
            ]

        if primary_keys:

            result.append("")

            result.append(
                "Primary Key:"
            )

            for pk in primary_keys:

                result.append(
                    f"- {pk}"
                )

        # ==========================================
        # COLUMNS
        # ==========================================

        result.append("")

        result.append(
            "Columns:"
        )

        for column in table["columns"]:

            column_name = column["name"]

            line = (
                f"- {column_name}"
            )

            if column.get("type"):

                line += (
                    f" ({column['type']})"
                )

            if column.get(
                "description"
            ):

                line += (
                    f" : "
                    f"{column['description']}"
                )

            result.append(line)

        # ==========================================
        # FOREIGN KEYS
        # ==========================================

        foreign_keys = table.get(
            "foreign_keys",
            []
        )

        if foreign_keys:

            result.append("")

            result.append(
                "Foreign Keys:"
            )

            for fk in foreign_keys:

                # Mendukung struktur:
                # referenced_table /
                # referenced_column

                if (
                    "referenced_table"
                    in fk
                    and
                    "referenced_column"
                    in fk
                ):

                    result.append(
                        f"- {fk['column']} "
                        f"-> "
                        f"{fk['referenced_table']}."
                        f"{fk['referenced_column']}"
                    )

                # Fallback jika schema kamu
                # menggunakan references
                elif "references" in fk:

                    result.append(
                        f"- {fk['column']} "
                        f"-> "
                        f"{fk['references']}"
                    )

        result.append("")

    return "\n".join(result)

import re


def build_prompt_from_template(
    template,
    database,
    schema,
    question
):

    schema_text = schema_to_text(schema)

    prompt = (
        template
        .replace("{{database}}", database)
        .replace("{{schema}}", schema_text)
        .replace("{{question}}", question)
    )

    prompt = clean_prompt(prompt)

    return prompt

def clean_prompt(text):

    # Hilangkan spasi di awal/akhir setiap baris
    lines = [line.strip() for line in text.splitlines()]

    cleaned = []
    blank = False

    for line in lines:

        if line == "":
            if not blank:
                cleaned.append("")
            blank = True

        else:
            cleaned.append(line)
            blank = False

    return "\n".join(cleaned).strip()