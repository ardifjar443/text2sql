import json
from pathlib import Path
from datetime import datetime
from unittest import result
import uuid
import time

from services.prompt_service import (
    load_prompt,
    build_prompt_from_template
)

from services.schema_service import (
    load_schema
)

from services.embedding_service import (
    embed_question,
    retrieve_tables,
    retrieve_columns
)

from services.mini_schema_service import (
    build_mini_schema
)

from services.dataset_service import get_ground_truth_sql

from services.llm_service import generate_sql
from services.evaluation_service import evaluate_sql, extract_sql

CONFIG_DIR = Path("data/experiment")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {

    "experiment_name": "",

    "schema_source": "full",

    "llm_model": "",

    "embedding_model": "",

    "retrieval_method": "top5",

    "temperature": 0,

    "max_token": 2048,

    "self_correction": True

}

HISTORY_DIR = CONFIG_DIR / "history" / "single"

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_experiment_config():

    if not CONFIG_FILE.exists():

        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, encoding="utf8") as f:

        return json.load(f)


def save_experiment_config(form):

    config = {

        "experiment_name": form["experiment_name"],

        "schema_source": form["schema_source"],

        "llm_model": form["llm_model"],

        "embedding_model": form.get("embedding_model"),

        "retrieval_method": form.get("retrieval_method"),

        "temperature": float(form["temperature"]),

        "max_token": int(form["max_token"]),

        "self_correction": form.get("self_correction") == "on"

    }

    with open(CONFIG_FILE, "w", encoding="utf8") as f:

        json.dump(

            config,

            f,

            indent=4,

            ensure_ascii=False

        )


def get_experiment_summary():

    history = CONFIG_DIR / "history"

    history.mkdir(exist_ok=True)

    return {

        "total_experiment": len(list(history.iterdir()))

    }


# =====================================================
# MAIN PIPELINE
# =====================================================

def run_pipeline(

    question,

    retrieval,

    embedding_model,

    llm_model,

    temperature,

    max_token,
    save_history=True

):
    pipeline_start = time.perf_counter()
    logs = []

    selected_tables = []

    selected_columns = []

    mini_schema = None

    logs.append("Load Prompt Template")
    print("Load Prompt Template")

    template = load_prompt()

    if template is None:

        raise Exception("Prompt template belum tersedia.")

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
    # FULL SCHEMA
    # ============================================
    retrieval_start = time.perf_counter()
    if retrieval.lower() == "full":

        logs.append("Use Full Schema")

        mini_schema = full_schema

    
    # ============================================
    # EMBEDDING RETRIEVAL
    # ============================================

    else:

        logs.append("Generate Question Embedding")

        question_embedding = embed_question(

            question,

            embedding_model

        )

        logs.append("Retrieve Tables")

        selected_tables = retrieve_tables(

            question_embedding,

            strategy=retrieval,

            # top_k=top_k

        )

        logs.append("Retrieve Columns")

        selected_columns = retrieve_columns(

            question_embedding,

            selected_tables,

            strategy="top5",

            # top_k=top_k

        )

        logs.append("Build Mini Schema")

        mini_schema = build_mini_schema(

            selected_tables,

            selected_columns

        )
    retrieval_time = time.perf_counter() - retrieval_start
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
    logs.append(
        "Generate SQL"
    )
    print("Generate SQL")
    llm_start = time.perf_counter()
    llm_result = generate_sql(

        prompt=prompt,

        model=llm_model,

        temperature=temperature,

        max_token=max_token

    )

    logs.append(
        "SQL Generated"
    )
    llm_generation_time = time.perf_counter() - llm_start
    generated_sql = extract_sql(llm_result["sql"])

    logs.append("Load Ground Truth")
    
    ground_truth_sql = get_ground_truth_sql(question)

    logs.append("Evaluate SQL")
    print("Evaluate SQL")
    evaluation_start = time.perf_counter()

    evaluation = None

    if ground_truth_sql:

        evaluation = evaluate_sql(
            generated_sql,
            ground_truth_sql
        )

    else:

        logs.append(
            "Ground Truth tidak ditemukan"
        )

    logs.append("Finished")
    
    evaluation_time = time.perf_counter() - evaluation_start
    total_pipeline_time = (
            time.perf_counter()
            - pipeline_start
        )
    
    result = {

        "question": question,

        "retrieval": retrieval,

        "embedding_model": embedding_model,

        "llm_model": llm_model,

        "prompt": prompt,

        "generated_sql": generated_sql,

        "ground_truth_sql": ground_truth_sql,

        "evaluation": evaluation,

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

        "selected_tables": selected_tables,

        "selected_columns": selected_columns,

        "mini_schema": mini_schema,

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
        
        
                "evaluation_time":
                    round(evaluation_time, 4),
        
                "total_pipeline_time":
                    round(total_pipeline_time, 4)
        
            }

    }
   
    if save_history:
        save_path = save_single_experiment(result)
        result["history_file"] = save_path
    
    return {

    "prompt": prompt,

    "generated_sql":

        generated_sql,

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

        len(

            mini_schema["tables"]

        ),

    "column_count":

        sum(

            len(t["columns"])

            for t in mini_schema["tables"]

        ),
    "ground_truth_sql": ground_truth_sql,

    "evaluation": evaluation,
    "timing": {

        "retrieval_time":
            round(retrieval_time, 4),

        "prompt_build_time":
            round(prompt_build_time, 4),

        "llm_generation_time":
            round(llm_generation_time, 4),


        "evaluation_time":
            round(evaluation_time, 4),

        "total_pipeline_time":
            round(total_pipeline_time, 4)

    }

}
    
def save_single_experiment(result):

    experiment_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = HISTORY_DIR / f"{experiment_id}.json"
    

    history = {

        "experiment_id":
            experiment_id,

        "created_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "question":
            result["question"],

        "retrieval":
            result["retrieval"],

        "embedding_model":
            result["embedding_model"],

        "llm_model":
            result["llm_model"],

        "generated_sql":
            result["generated_sql"],

        "ground_truth_sql":
            result["ground_truth_sql"],

        "exact_match":
            result["evaluation"]["exact_match"],

        "execution_accuracy":
            result["evaluation"]["execution_accuracy"],

        "table_count":
            result["table_count"],
            
        
        "selected_tables":

            result["selected_tables"],

        "selected_columns":

            result["selected_columns"],

        "column_count":
            result["column_count"],

        "prompt_tokens":
            result["llm_statistics"]["prompt_tokens"],

        "completion_tokens":
            result["llm_statistics"]["completion_tokens"],

        "total_tokens":
            result["llm_statistics"]["total_tokens"],

        "latency":
            result["llm_statistics"]["latency"],
        "timing": result["timing"],
            
                

    }

    with open(

        file_path,

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            history,

            f,

            indent=4,

            ensure_ascii=False

        )

    return str(file_path)