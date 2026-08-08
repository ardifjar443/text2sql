from flask import Blueprint
from flask import render_template

from services.dataset_service import load_dataset
from services.schema_service import load_schema
# from services.embedding_service import embedding_status

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def dashboard():

    df = load_dataset()

    dataset_count = len(df)

    schema = load_schema()

    if schema:

        schema_count = len(schema["tables"])

    else:

        schema_count = 0

    return render_template(

        "dashboard.html",

        dataset_count=dataset_count,

        schema_count=schema_count,

        # embedding_status=embedding_status(),

        experiment_count=0

    )