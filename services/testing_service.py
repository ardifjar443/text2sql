import time

from services.prompt_service import (
    load_prompt,
    build_prompt_from_template
)

from services.schema_service import (
    load_schema
)
import pymysql
from services.embedding_service import (
    embed_question,
    retrieve_tables,
    retrieve_columns
)

from services.mini_schema_service import (
    build_mini_schema
)

from services.llm_service import generate_sql
from services.evaluation_service import evaluate_sql, extract_sql, execute_sql

from config import Config


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():
    """
    Membuat koneksi ke database MySQL.
    """

    return pymysql.connect(
        host=Config.DB_HOST,
        port=int(Config.DB_PORT),
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


def run_testing(
    question,
    retrieval,
    embedding_model,
    llm_model,
    temperature,
    max_token
):
    pipeline_start = time.perf_counter()

    logs = []

    selected_tables = []
    selected_columns = []
    mini_schema = None

    # ============================================
    # LOAD PROMPT TEMPLATE
    # ============================================

    logs.append("Load Prompt Template")
    print("Load Prompt Template")

    template = load_prompt()

    if template is None:
        raise Exception("Prompt template belum tersedia.")

    # ============================================
    # LOAD DATABASE SCHEMA
    # ============================================

    logs.append("Load Database")
    print("Load Database")

    full_schema = load_schema()

    if full_schema is None:
        raise Exception("Schema belum tersedia.")

    database = full_schema.get(
        "database",
        "-"
    )

    # ============================================
    # SCHEMA RETRIEVAL
    # ============================================

    retrieval_start = time.perf_counter()

    if retrieval.lower() == "full":

        logs.append("Use Full Schema")
        print("Use Full Schema")

        mini_schema = full_schema

    else:

        # ----------------------------------------
        # QUESTION EMBEDDING
        # ----------------------------------------

        logs.append("Generate Question Embedding")
        print("Generate Question Embedding")

        question_embedding = embed_question(
            question,
            embedding_model
        )

        # ----------------------------------------
        # RETRIEVE TABLES
        # ----------------------------------------

        logs.append("Retrieve Tables")
        print("Retrieve Tables")

        selected_tables = retrieve_tables(
            question_embedding,
            strategy=retrieval
        )

        # ----------------------------------------
        # RETRIEVE COLUMNS
        # ----------------------------------------

        logs.append("Retrieve Columns")
        print("Retrieve Columns")

        selected_columns = retrieve_columns(
            question_embedding,
            selected_tables,
            strategy="top5"
        )

        # ----------------------------------------
        # BUILD MINI SCHEMA
        # ----------------------------------------

        logs.append("Build Mini Schema")
        print("Build Mini Schema")

        mini_schema = build_mini_schema(
            selected_tables,
            selected_columns
        )

    retrieval_time = time.perf_counter() - retrieval_start
    
    print("\n========== EMBEDDING DEBUG ==========")
    print("Embedding model :", embedding_model)
    print("Embedding type  :", type(question_embedding))
    print("Embedding length:", len(question_embedding))
    print("Embedding first :", question_embedding[:5])
    print("=====================================\n")

    # ============================================
    # BUILD PROMPT
    # ============================================

    logs.append("Build Prompt")
    print("Build Prompt")

    prompt_start = time.perf_counter()

    prompt = build_prompt_from_template(
        template=template,
        database=database,
        schema=mini_schema,
        question=question
    )

    prompt_build_time = time.perf_counter() - prompt_start

    # ============================================
    # GENERATE SQL
    # ============================================

    logs.append("Generate SQL")
    print("Generate SQL")

    llm_start = time.perf_counter()

    llm_result = generate_sql(
        prompt=prompt,
        model=llm_model,
        temperature=temperature,
        max_token=max_token
    )

    llm_generation_time = time.perf_counter() - llm_start

    logs.append("SQL Generated")

    generated_sql = extract_sql(
        llm_result["sql"]
    )

    # ============================================
    # FINISHED
    # ============================================

    logs.append("Finished")

    total_pipeline_time = (
        time.perf_counter()
        - pipeline_start
    )

    # ============================================
    # RESULT
    # ============================================

    return {

        "question": question,

        "retrieval": retrieval,

        "embedding_model": embedding_model,

        "llm_model": llm_model,

        "prompt": prompt,

        "generated_sql": generated_sql,

        "llm_statistics": {

            "prompt_tokens":
                llm_result["prompt_tokens"],

            "completion_tokens":
                llm_result["completion_tokens"],

            "total_tokens":
                llm_result["total_tokens"],

            "latency":
                llm_result["latency"]

        },

        "logs": logs,

        "selected_tables":
            selected_tables,

        "selected_columns":
            selected_columns,

        "mini_schema":
            mini_schema,

        "table_count":
            len(mini_schema["tables"]),

        "column_count":
            sum(
                len(t["columns"])
                for t in mini_schema["tables"]
            ),

        "timing": {

            "retrieval_time":
                round(retrieval_time, 4),

            "prompt_build_time":
                round(prompt_build_time, 4),

            "llm_generation_time":
                round(llm_generation_time, 4),

            "total_pipeline_time":
                round(total_pipeline_time, 4)

        }

    }
    

def execute_generated_sql(sql):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        return {

            "success": True,

            "rows": rows,

            "row_count": len(rows)

        }

    except Exception as e:

        return {

            "success": False,

            "rows": [],

            "row_count": 0,

            "error": str(e)

        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

def run_web_testing(
    question,
    retrieval,
    embedding_model,
    llm_model,
    temperature,
    max_token
):

    # ============================================
    # GENERATE SQL
    # ============================================

    result = run_testing(
        question=question,
        retrieval=retrieval,
        embedding_model=embedding_model,
        llm_model=llm_model,
        temperature=temperature,
        max_token=max_token
    )

    generated_sql = result["generated_sql"]

    # ============================================
    # EXECUTE SQL
    # ============================================

    execution = execute_generated_sql(
        generated_sql
    )

    # ============================================
    # RETURN WEBSITE RESULT
    # ============================================

    return {

        "question":
            question,

        "generated_sql":
            generated_sql,

        "selected_tables":
            result["selected_tables"],

        "selected_columns":
            result["selected_columns"],

        "table_count":
            result["table_count"],

        "column_count":
            result["column_count"],

        "execution":
            execution,

        "llm_statistics":
            result["llm_statistics"],

        "timing":
            result["timing"]

    }