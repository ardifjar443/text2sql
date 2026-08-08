from flask import Blueprint
from flask import render_template

from services.dataset_service import load_dataset
# from services.embedding_service import embedding_status

embedding_bp = Blueprint(
    "embedding",
    __name__,
    url_prefix="/embedding"
)


@embedding_bp.route("/")
def index():

    models = [

        "openai/text-embedding-3-small",

        "openai/text-embedding-3-large",

        "qwen/qwen3-embedding-8b",

        "baai/bge-large-en-v1.5"

    ]

    df = load_dataset()

    questions = df.to_dict(
        orient="records"
    )

    return render_template(

        "embedding/index.html",

        models=models,

        questions=questions,

        # status=embedding_status()

    )