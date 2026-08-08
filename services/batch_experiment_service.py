import json

from pathlib import Path

from datetime import datetime

from services.dataset_service import load_dataset

from services.experiment_service import run_pipeline
from openpyxl import Workbook

BATCH_HISTORY_DIR = Path(

    "data/experiment/history/batch"

)

BATCH_HISTORY_DIR.mkdir(

    parents=True,

    exist_ok=True

)

def save_batch_experiment(

    summary,

    details

):

    experiment_id = datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )

    folder = BATCH_HISTORY_DIR / experiment_id

    folder.mkdir(

        parents=True,

        exist_ok=True

    )

    with open(

        folder / "summary.json",

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            summary,

            f,

            indent=4,

            ensure_ascii=False

        )

    with open(

        folder / "detail.json",

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            details,

            f,

            indent=4,

            ensure_ascii=False

        )

    return folder

def save_batch_excel(

    folder,

    details

):

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Result"

    worksheet.append([

        "No",

        "Question",

        "Generated SQL",

        "Ground Truth SQL",

        "Exact Match",

        "Execution Accuracy",

        "Latency",

        "Prompt Tokens",

        "Completion Tokens",

        "Total Tokens"

    ])

    for item in details:

        worksheet.append([

            item["no"],

            item["question"],

            item["generated_sql"],

            item["ground_truth_sql"],

            item["exact_match"],

            item["execution_accuracy"],

            item["latency"],

            item["prompt_tokens"],

            item["completion_tokens"],

            item["total_tokens"]

        ])

    excel_path = folder / "result.xlsx"

    workbook.save(excel_path)

    return excel_path

def run_batch(

    retrieval,

    embedding_model,

    llm_model,

    temperature,

    max_token

):

    dataset = load_dataset()

    if dataset.empty:

        raise Exception(

            "Dataset belum tersedia."

        )

    results = []

    total_question = len(dataset)

    exact_match = 0

    execution_accuracy = 0

    total_latency = 0

    total_prompt_token = 0

    total_completion_token = 0

    total_total_token = 0

    # =====================================
    # LOOP SELURUH PERTANYAAN
    # =====================================
    
    print("model llm :", llm_model)
    REQUEST_COUNT = 1

    for index, row in dataset.iterrows():
        progress = (
                REQUEST_COUNT / total_question * 100
                if total_question > 0 else 0
            )
        print(
                f"[{REQUEST_COUNT}/{total_question}] "
                f"({progress:.1f}%) "
            )
        REQUEST_COUNT += 1

        question = row["Question"]

        result = run_pipeline(

            question=question,

            retrieval=retrieval,

            embedding_model=embedding_model,

            llm_model=llm_model,

            temperature=temperature,

            max_token=max_token,

            save_history=False

        )

        evaluation = result["evaluation"]

        statistics = result["llm_statistics"]

        if evaluation["exact_match"]:

            exact_match += 1

        if evaluation["execution_accuracy"]:

            execution_accuracy += 1

        total_latency += statistics["latency"]

        total_prompt_token += statistics["prompt_tokens"]

        total_completion_token += statistics["completion_tokens"]

        total_total_token += statistics["total_tokens"]

        results.append({

            "no": index + 1,

            "question": question,

            "generated_sql": result["generated_sql"],

            "ground_truth_sql": result["ground_truth_sql"],

            "exact_match": evaluation["exact_match"],

            "execution_accuracy": evaluation["execution_accuracy"],

            "latency": statistics["latency"],

            "prompt_tokens": statistics["prompt_tokens"],

            "completion_tokens": statistics["completion_tokens"],

            "total_tokens": statistics["total_tokens"],

            # ===============================
            # Retrieval Detail
            # ===============================

            "table_count": len(result.get("selected_tables", [])),

            "column_count": len(result.get("selected_columns", [])),
            "retrieval_time":
                result["timing"]["retrieval_time"],

            "prompt_build_time":
                result["timing"]["prompt_build_time"],

            "llm_generation_time":
                result["timing"]["llm_generation_time"],


            "evaluation_time":
                result["timing"]["evaluation_time"],

            "total_pipeline_time":
                result["timing"]["total_pipeline_time"],

            "selected_tables": result.get(
                "selected_tables",
                []
            ),

            "selected_columns": result.get(
                "selected_columns",
                []
            )

})

    # =====================================
    # SUMMARY
    # =====================================

    summary = {
        "model llm ": llm_model,
        "embedding model": embedding_model,
        "retrieval": retrieval,
        "created_at":

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            ),

        "total_question":

            total_question,

        "exact_match":

            exact_match,

        "execution_accuracy":

            execution_accuracy,

        "exact_match_percentage":

            round(

                exact_match / total_question * 100,

                2

            ),

        "execution_accuracy_percentage":

            round(

                execution_accuracy / total_question * 100,

                2

            ),

        "average_latency":

            round(

                total_latency / total_question,

                3

            ),

        "average_prompt_tokens":

            round(

                total_prompt_token / total_question,

                2

            ),

        "average_completion_tokens":

            round(

                total_completion_token / total_question,

                2

            ),

        "average_total_tokens":

            round(

                total_total_token / total_question,

                2

            )

    }

    # =====================================
    # SAVE
    # =====================================

    history_folder = save_batch_experiment(

        summary,

        results

    )

    excel_file = save_batch_excel(

        history_folder,

        results

    )

    # =====================================
    # RETURN
    # =====================================

    return {

        "summary": summary,

        "history": str(history_folder),

        "excel": str(excel_file),

        "batch_id": history_folder.name

    }