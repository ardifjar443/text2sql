from flask import Blueprint, send_file
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from config import Config

from services.schema_service import get_current_database
from services.embedding_service import get_embedding_metadata
from services.dataset_service import get_dataset_metadata, load_dataset
from services.experiment_service import (
    load_experiment_config,
    save_experiment_config,
    get_experiment_summary,
    run_pipeline
)

from flask import jsonify



from services.prompt_service import (
    build_prompt_config,
    build_experiment_prompt
)

from services.schema_service import (

    load_schema,

    build_full_schema,

    build_mini_schema,

    get_current_database

)
from services.evaluation_service import evaluate_sql
from services.batch_experiment_service import run_batch, BATCH_HISTORY_DIR



experiment_bp = Blueprint(
    "experiment",
    __name__,
    url_prefix="/experiment"
)


from config import Config


@experiment_bp.route("/")
def index():

    dataset = load_dataset()

    return render_template(

        "experiment/index.html",

        dataset=dataset,

        llm_models=Config.LLM_MODELS,

        embedding_models=Config.EMBEDDING_MODELS,

        retrievals=[
            
            {
                "id": "adaptive_gap",
                "name": "Adaptive Gap"
            },

            {
                "id": "full",
                "name": "Full Schema"
            },

            {
                "id": "top1",
                "name": "Top 1"
            },

            {
                "id": "top3",
                "name": "Top 3"
            },

            {
                "id": "top5",
                "name": "Top 5"
            },

            {
                "id": "top7",
                "name": "Top 7"
            },

            

            {
                "id": "adaptive_mean",
                "name": "Adaptive Mean"
            },

            {
                "id": "adaptive_mean_sd1",
                "name": "Adaptive Mean + SD1"
            },

            {
                "id": "adaptive_percentile75",
                "name": "Adaptive Percentile 75"
            }

        ]

    )
    


from flask import request, jsonify

@experiment_bp.post("/run_pipeline")
def execute_pipeline():

    question = request.form.get("question")

    retrieval = request.form.get("retrieval")

    embedding_model = request.form.get("embedding_model")

    top_k = int(
        request.form.get("top_k", 5)
    )
    
    llm_model = request.form.get(

        "llm_model"

    )

    temperature = float(

        request.form.get(

            "temperature",

            0

        )

    )

    max_token = int(

        request.form.get(

            "max_token",

            2048

        )

    )

    result = run_pipeline(

        question=question,

        retrieval=retrieval,

        embedding_model=embedding_model,

        llm_model=llm_model,

        temperature=temperature,

        max_token=max_token

    )
    

    return jsonify(result)
@experiment_bp.route(
    "/save",
    methods=["POST"]
)
def save():

    save_experiment_config(

        request.form

    )

    flash(

        "Configuration berhasil disimpan.",

        "success"

    )

    return redirect(

        url_for(

            "experiment.index"

        )

    )
    
@experiment_bp.route(
    "/preview",
    methods=["POST"]
)
def preview():

    question = request.form["question"]

    retrieval = request.form.get(

        "retrieval",

        "none"

    )

    metadata = get_current_database()

    full_schema = load_schema()

    mini_schema = build_mini_schema(question)

    config = build_prompt_config(

        retrieval=retrieval,

        few_shot=False,

        version="v1"

    )

    result = build_experiment_prompt(

        metadata,

        full_schema,

        mini_schema,

        question,

        config

    )

    return render_template(

        "experiment/prompt_preview.html",

        prompt=result["prompt"],

        summary=result["statistics"],

        config=result["config"]

    )
    
@experiment_bp.post("/run_batch")
def run_batch_route():

    retrieval = request.form.get("retrieval")

    embedding_model = request.form.get("embedding_model")

    llm_model = request.form.get("llm_model")

    temperature = float(

        request.form.get(

            "temperature",

            0

        )

    )

    max_token = int(

        request.form.get(

            "max_token",

            2048

        )

    )

    result = run_batch(

        retrieval=retrieval,

        embedding_model=embedding_model,

        llm_model=llm_model,

        temperature=temperature,

        max_token=max_token

    )

    return jsonify(result)


@experiment_bp.get(

    "/download_batch/<batch_id>"

)

def download_batch(

    batch_id

):

    folder = (

        BATCH_HISTORY_DIR

        / batch_id

    )

    return send_file(

        folder / "result.xlsx",

        as_attachment=True

    )