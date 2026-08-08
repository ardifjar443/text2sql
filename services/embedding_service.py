import json
import shutil

from pathlib import Path
from datetime import datetime

from matplotlib import lines

from services.openrouter_service import OpenRouterClient


# ==========================================================
# OPENROUTER CLIENT
# ==========================================================

client = OpenRouterClient()


# ==========================================================
# PATH CONFIGURATION
# ==========================================================

SCHEMA_PATH = Path(
    "data/schema/schema_metadata.json"
)

OUTPUT_DIR = Path(
    "data/schema/embeddings"
)

CURRENT_DIR = OUTPUT_DIR / "current"

HISTORY_DIR = OUTPUT_DIR / "history"

CURRENT_METADATA = CURRENT_DIR / "metadata.json"


CURRENT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)


TABLE_OUTPUT = CURRENT_DIR / "table_embeddings.json"

COLUMN_OUTPUT = CURRENT_DIR / "column_embeddings.json"

METADATA_OUTPUT = CURRENT_DIR / "metadata.json"

SENSITIVE_COLUMNS = {
    "nik",
    "no_kk",
    "no_rekening",
    "idsemesta"
}


# ==========================================================
# LOAD SCHEMA
# ==========================================================

def load_schema():

    with open(
        SCHEMA_PATH,
        encoding="utf8"
    ) as f:

        return json.load(f)


# ==========================================================
# CREATE HISTORY VERSION
# ==========================================================

def create_history_folder():

    version = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    folder = HISTORY_DIR / version

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return version, folder


# ==========================================================
# SAVE JSON
# ==========================================================

def save_json(

    data,

    output_path

):

    with open(

        output_path,

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )


# ==========================================================
# LOAD JSON
# ==========================================================

def load_json(

    file_path

):

    if not Path(

        file_path

    ).exists():

        return None

    with open(

        file_path,

        encoding="utf8"

    ) as f:

        return json.load(f)


# ==========================================================
# BUILD METADATA
# ==========================================================

def build_metadata(
    version,
    model,
    dimension,
    table_count,
    column_count,
    schema
):

    return {

        "version": version,

        "database": schema.get(
            "database",
            "Unknown"
        ),

        "description": schema.get(
            "description",
            "-"
        ),

        "schema_version": schema.get(
            "version",
            "1.0"
        ),

        "generator": "Text2SQL Studio",

        "model": model,

        "dimension": dimension,

        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "table_count": table_count,

        "column_count": column_count

    }


# ==========================================================
# SAVE CURRENT FILES
# ==========================================================

def save_current(

    metadata,

    table_embeddings,

    column_embeddings

):

    save_json(

        metadata,

        METADATA_OUTPUT

    )

    save_json(

        table_embeddings,

        TABLE_OUTPUT

    )

    save_json(

        column_embeddings,

        COLUMN_OUTPUT

    )


# ==========================================================
# SAVE HISTORY
# ==========================================================

def save_history(

    history_folder,

    metadata,

    table_embeddings,

    column_embeddings

):

    save_json(

        metadata,

        history_folder / "metadata.json"

    )

    save_json(

        table_embeddings,

        history_folder / "table_embeddings.json"

    )

    save_json(

        column_embeddings,

        history_folder / "column_embeddings.json"

    )


# ==========================================================
# GET CURRENT METADATA
# ==========================================================

def get_embedding_metadata():

    return load_json(

        METADATA_OUTPUT

    )


# ==========================================================
# GET HISTORY
# ==========================================================



# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text):

    if text is None:

        return ""

    return " ".join(

        str(text).strip().split()

    )


# ==========================================================
# CHECK FOREIGN KEY
# ==========================================================

def is_foreign_key(

    table,

    column_name

):

    for fk in table.get(

        "foreign_keys",

        []

    ):

        if fk["column"] == column_name:

            return True

    return False


# ==========================================================
# BUILD TABLE EMBEDDING TEXT
# ==========================================================

def build_table_text(table):

    schema = load_schema()

    database = schema.get("database", "Unknown")
    domain = schema.get("description", "")
    
    lines = []

    # lines.append(f"DATABASE : {database}")
    # lines.append(f"DOMAIN : {domain}")

    lines.append("")

    lines.append(

        f"TABLE : {table['table']}"

    )

    lines.append(

        f"DESCRIPTION : {normalize_text(table['description'])}"

    )

    lines.append("")

    lines.append(

        f"PRIMARY KEY : {table['primary_key']}"

    )

    foreign_keys = table.get(

        "foreign_keys",

        []

    )

    if foreign_keys:

        lines.append("")

        lines.append(

            "FOREIGN KEYS :"

        )

        for fk in foreign_keys:

            lines.append(

                f"- {fk['column']} -> {fk['references']}"

            )

    lines.append("")

    lines.append(

        "COLUMNS :"

    )

    for column in table["columns"]:

        lines.append(

            f"- {column['name']} ({column['type']})"

        )
        lines.append(
        f"  Description: {normalize_text(column['description'])}"
    )

    return "\n".join(lines)


# ==========================================================
# BUILD COLUMN EMBEDDING TEXT
# ==========================================================

def build_column_text(
    table,
    column
):

    schema = load_schema()

    database = schema.get(
        "database",
        "Unknown"
    )

    domain = schema.get(
        "description",
        ""
    )

    lines = []

    # lines.append(
    #     f"DATABASE : {database}"
    # )

    # lines.append(
    #     f"DOMAIN : {domain}"
    # )

    # lines.append("")

    lines.append(
        f"TABLE : {table['table']}"
    )

    lines.append(
        f"TABLE DESCRIPTION : "
        f"{normalize_text(table['description'])}"
    )

    lines.append("")

    lines.append(
        f"COLUMN : {column['name']}"
    )

    lines.append(
        f"TYPE : {column['type']}"
    )

    lines.append(
        f"DESCRIPTION : "
        f"{normalize_text(column.get('description', ''))}"
    )

    # ==========================================
    # NORMALIZE PRIMARY KEY
    # ==========================================

    primary_keys = table.get(
        "primary_key",
        []
    )

    if isinstance(primary_keys, str):
        primary_keys = [primary_keys]

    if primary_keys is None:
        primary_keys = []

    # ==========================================
    # FOREIGN KEYS
    # ==========================================

    foreign_keys = table.get(
        "foreign_keys",
        []
    )

    if foreign_keys is None:
        foreign_keys = []

    # ==========================================
    # ROLE
    # ==========================================

    lines.append("")

    if column["name"] in primary_keys:

        lines.append(
            "ROLE : PRIMARY KEY"
        )

    elif any(
        fk.get("column") == column["name"]
        for fk in foreign_keys
    ):

        fk = next(
            fk
            for fk in foreign_keys
            if fk.get("column") == column["name"]
        )

        lines.append(
            f"ROLE : FOREIGN KEY -> "
            f"{fk.get('references', '')}"
        )

    else:

        lines.append(
            "ROLE : NORMAL COLUMN"
        )

    return "\n".join(lines)

# ==========================================================
# GENERATE TABLE EMBEDDINGS
# ==========================================================

def generate_table_embeddings(model):

    schema = load_schema()

    embeddings = []

    total = len(
        schema["tables"]
    )

    print("\n" + "=" * 60)
    print("Generating Table Embeddings")
    print("=" * 60)

    for index, table in enumerate(

        schema["tables"],

        start=1

    ):

        print(

            f"[{index}/{total}] {table['table']}"

        )

        text = build_table_text(

            table

        )

        vector = client.embedding(

            text,

            model

        )

        embeddings.append({

            "table": table["table"],

            "description": table["description"],

            "primary_key": table["primary_key"],

            "foreign_keys": table.get(

                "foreign_keys",

                []

            ),

            "embedding": vector

        })

    print(

        f"\nTotal Table : {len(embeddings)}"

    )

    return embeddings


# ==========================================================
# GENERATE COLUMN EMBEDDINGS
# ==========================================================

def generate_column_embeddings(model):

    schema = load_schema()

    embeddings = []

    total = sum(
        len(table["columns"])
        for table in schema["tables"]
    )

    current = 0

    print("\n" + "=" * 60)
    print("Generating Column Embeddings")
    print("=" * 60)

    for table in schema["tables"]:

        # ==========================================
        # NORMALIZE PRIMARY KEY
        # ==========================================

        primary_keys = table.get(
            "primary_key",
            []
        )

        # Jika PK berupa string
        if isinstance(primary_keys, str):
            primary_keys = [primary_keys]

        # Jika PK kosong / None
        if primary_keys is None:
            primary_keys = []

        # ==========================================
        # FOREIGN KEYS
        # ==========================================

        foreign_keys = table.get(
            "foreign_keys",
            []
        )

        if foreign_keys is None:
            foreign_keys = []

        # Buat set nama kolom FK
        foreign_key_columns = {
            fk["column"]
            for fk in foreign_keys
            if "column" in fk
        }

        # ==========================================
        # PROCESS COLUMNS
        # ==========================================

        for column in table["columns"]:

            current += 1

            column_name = column["name"]

            print(
                f"[{current}/{total}] "
                f"{table['table']}.{column_name}"
            )

            # ======================================
            # CHECK PRIMARY KEY
            # ======================================

            is_primary_key = (
                column_name in primary_keys
            )

            # ======================================
            # CHECK FOREIGN KEY
            # ======================================

            is_fk = (
                column_name in foreign_key_columns
            )

            # ======================================
            # BUILD EMBEDDING TEXT
            # ======================================

            text = build_column_text(
                table,
                column
            )

            vector = client.embedding(
                text,
                model
            )

            embeddings.append({

                "table": table["table"],

                "column": column_name,

                "type": column["type"],

                "description": column.get(
                    "description",
                    ""
                ),

                "primary_key": is_primary_key,

                "foreign_key": is_fk,

                "embedding": vector

            })

            # ======================================
            # DEBUG
            # ======================================

            if is_primary_key:

                print(
                    f"    → PRIMARY KEY"
                )

            if is_fk:

                print(
                    f"    → FOREIGN KEY"
                )

    print(
        f"\nTotal Column : {len(embeddings)}"
    )

    return embeddings

# ==========================================================
# QUESTION EMBEDDING
# ==========================================================

def embed_question(

    question,

    model

):

    question = normalize_text(

        question

    )

    return client.embedding(

        question,

        model

    )


# ==========================================================
# GENERATE SCHEMA EMBEDDING
# ==========================================================

def generate_schema_embeddings(

    model

):

    print("\n" + "=" * 60)
    print("GENERATE SCHEMA EMBEDDING")
    print("=" * 60)

    version, history_folder = create_history_folder()

    table_embeddings = generate_table_embeddings(

        model

    )

    column_embeddings = generate_column_embeddings(

        model

    )

    dimension = len(

        table_embeddings[0]["embedding"]

    ) if table_embeddings else 0

    schema = load_schema()

    metadata = build_metadata(
        version=version,
        model=model,
        dimension=dimension,
        table_count=len(table_embeddings),
        column_count=len(column_embeddings),
        schema=schema
    )

    save_current(

        metadata,

        table_embeddings,

        column_embeddings

    )

    save_history(

        history_folder,

        metadata,

        table_embeddings,

        column_embeddings

    )

    print("\nEmbedding selesai.")

    print(f"Version : {version}")

    return metadata

def use_embedding(version):

    current_schema = load_schema()

    current_database = current_schema.get(
        "database"
    )

    current_schema_version = current_schema.get(
        "version"
    )

    source = HISTORY_DIR / version

    if not source.exists():

        raise Exception(
            "Embedding history tidak ditemukan."
        )

    metadata_file = source / "metadata.json"

    table_file = source / "table_embeddings.json"

    column_file = source / "column_embeddings.json"

    if not metadata_file.exists():

        raise Exception(
            "Metadata embedding tidak ditemukan."
        )

    if not table_file.exists():

        raise Exception(
            "Table embedding tidak ditemukan."
        )

    if not column_file.exists():

        raise Exception(
            "Column embedding tidak ditemukan."
        )

    with open(

        metadata_file,

        encoding="utf8"

    ) as f:

        metadata = json.load(f)

    embedding_database = metadata.get(
        "database"
    )

    embedding_schema_version = metadata.get(
        "schema_version"
    )

    if embedding_database != current_database:

        raise Exception(

            f"Embedding dibuat untuk database '{embedding_database}', "
            f"sedangkan database aktif adalah '{current_database}'."

        )

    if (

        embedding_schema_version is not None
        and current_schema_version is not None
        and embedding_schema_version != current_schema_version

    ):

        raise Exception(

            "Schema version tidak cocok."

        )

    shutil.copy2(

        metadata_file,

        CURRENT_DIR / "metadata.json"

    )

    shutil.copy2(

        table_file,

        TABLE_OUTPUT

    )

    shutil.copy2(

        column_file,

        COLUMN_OUTPUT

    )

    return True

def get_embedding_history():

    histories = []

    if not HISTORY_DIR.exists():

        return histories

    folders = sorted(

        HISTORY_DIR.iterdir(),

        reverse=True

    )
    
    current = get_current_embedding()

    current_version = None

    if current:

        current_version = current.get(
            "version"
        )

    for folder in folders:

        metadata = load_json(

            folder / "metadata.json"

        )

        if metadata:

            histories.append({

            "version": folder.name,

            "database": metadata.get(
                "database",
                "-"
            ),

            "model": metadata.get(
                "model",
                "-"
            ),

            "dimension": metadata.get(
                "dimension",
                0
            ),

            "table_count": metadata.get(
                "table_count",
                0
            ),

            "column_count": metadata.get(
                "column_count",
                0
            ),

            "created_at": metadata.get(
                "created_at",
                "-"
            ),

            "schema_version": metadata.get(
                "schema_version",
                "-"
            ),

            "is_active":

                folder.name == current_version

        })

    return histories

import shutil

def use_embedding_version(version):

    source = HISTORY_DIR / version

    if not source.exists():

        raise Exception("Embedding version tidak ditemukan.")

    shutil.copy2(

        source / "table_embeddings.json",

        CURRENT_DIR / "table_embeddings.json"

    )

    shutil.copy2(

        source / "column_embeddings.json",

        CURRENT_DIR / "column_embeddings.json"

    )

    shutil.copy2(

        source / "metadata.json",

        CURRENT_DIR / "metadata.json"

    )
    
def get_current_embedding():

    if not CURRENT_METADATA.exists():

        return None

    with open(

        CURRENT_METADATA,

        encoding="utf8"

    ) as f:

        return json.load(f)
    
    
def delete_embedding(version):

    folder = HISTORY_DIR / version

    if not folder.exists():

        raise Exception(

            "Embedding tidak ditemukan."

        )

    shutil.rmtree(folder)
    
def clear_current_embedding():

    if CURRENT_DIR.exists():

        shutil.rmtree(CURRENT_DIR)

    CURRENT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def retrieve_tables(

    question_embedding,

    strategy="top5",

    top_k=5

):

    table_embeddings = load_table_embeddings()

    if not table_embeddings:

        raise Exception(

            "Table embedding belum tersedia."

        )

    similarities = []

    question_embedding = np.array(
        question_embedding
    ).reshape(1, -1)

    for table in table_embeddings:

        similarity = cosine_similarity(

            question_embedding,

            np.array(
                table["embedding"]
            ).reshape(1, -1)

        )[0][0]

        similarities.append({

            "table": table["table"],

            "similarity": float(similarity)

        })

    similarities.sort(

        key=lambda x: x["similarity"],

        reverse=True

    )

   # ===========================================
    # TOP K
    # ===========================================

    if strategy.startswith("top"):

        try:

            k = int(

                strategy.replace(
                    "top",
                    ""
                )

            )

        except:

            k = top_k

        return similarities[:k]


    # ===========================================
    # ADAPTIVE GAP
    # ===========================================

    elif strategy == "adaptive_gap":

        if len(similarities) < 2:

            return similarities

        gaps = []

        for i in range(

            len(similarities)-1

        ):

            gaps.append(

                similarities[i]["similarity"]

                -

                similarities[i+1]["similarity"]

            )

        max_gap_index = np.argmax(gaps)

        return similarities[:max_gap_index+1]


    # ===========================================
    # ADAPTIVE MEAN
    # ===========================================

    elif strategy == "adaptive_mean":

        sims = [

            s["similarity"]

            for s in similarities

        ]

        threshold = np.mean(sims)

        return [

            s

            for s in similarities

            if s["similarity"] >= threshold

        ]


    # ===========================================
    # ADAPTIVE MEAN + SD1
    # ===========================================

    elif strategy == "adaptive_mean_sd1":

        sims = [

            s["similarity"]

            for s in similarities

        ]

        threshold = (

            np.mean(sims)

            +

            np.std(sims)

        )

        return [

            s

            for s in similarities

            if s["similarity"] >= threshold

        ]


    # ===========================================
    # ADAPTIVE PERCENTILE 75
    # ===========================================

    elif strategy == "adaptive_percentile75":

        sims = [

            s["similarity"]

            for s in similarities

        ]

        threshold = np.percentile(

            sims,

            75

        )

        return [

            s

            for s in similarities

            if s["similarity"] >= threshold

        ]


    # ===========================================
    # DEFAULT
    # ===========================================

    return similarities

TABLE_OUTPUT = CURRENT_DIR / "table_embeddings.json"


def load_table_embeddings():

    if not TABLE_OUTPUT.exists():

        return []

    with open(

        TABLE_OUTPUT,

        encoding="utf8"

    ) as f:

        return json.load(f)
    
COLUMN_OUTPUT = CURRENT_DIR / "column_embeddings.json"


def load_column_embeddings():

    if not COLUMN_OUTPUT.exists():

        return []

    with open(
        COLUMN_OUTPUT,
        encoding="utf8"
    ) as f:

        return json.load(f)
    
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve_columns(
    question_embedding,
    selected_tables,
    strategy="top3",
    top_k=3
):

    column_embeddings = load_column_embeddings()

    if not column_embeddings:
        raise Exception(
            "Column embedding belum tersedia."
        )

    # =====================================================
    # TABEL YANG SUDAH TERPILIH
    # =====================================================

    table_names = {
        t["table"]
        for t in selected_tables
    }

    # =====================================================
    # KOLOM SENSITIF
    # =====================================================

    sensitive_columns = {
        "nik",
        "no_kk",
        "no_rekening",
        "idsemesta"
    }

    # =====================================================
    # EMBEDDING QUESTION
    # =====================================================

    question_embedding = np.array(
        question_embedding
    ).reshape(1, -1)

    # =====================================================
    # RETRIEVAL PER TABLE
    # =====================================================

    results = []

    for table_name in table_names:

        table_similarities = []

        for column in column_embeddings:

            # Hanya kolom dari tabel saat ini
            if column["table"] != table_name:
                continue

            # Jangan retrieve kolom sensitif
            if column["column"].lower() in sensitive_columns:
                continue

            # Jangan retrieve PRIMARY KEY
            if column.get("primary_key", False):
                continue

            # Jangan retrieve FOREIGN KEY
            if column.get("foreign_key", False):
                continue

            similarity = cosine_similarity(
                question_embedding,
                np.array(
                    column["embedding"]
                ).reshape(1, -1)
            )[0][0]

            table_similarities.append({
                "table": column["table"],
                "column": column["column"],
                "similarity": float(similarity)
            })

        # =================================================
        # SORT PER TABLE
        # =================================================

        table_similarities.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        # =================================================
        # TOP K PER TABLE
        # =================================================

        if strategy.startswith("top"):

            try:
                k = int(
                    strategy.replace(
                        "top",
                        ""
                    )
                )

            except ValueError:
                k = top_k

            table_similarities = (
                table_similarities[:k]
            )

        results.extend(
            table_similarities
        )

    return results