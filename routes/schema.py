from flask import Blueprint, Config, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from config import Config

from services.schema_service import (
    clear_current_embedding,
    load_schema,
    save_schema,
    schema_summary,
    get_current_database
)

# from services.embedding_service import get_embedding_metadata
# from services.embedding_service import generate_schema_embeddings
# from services.embedding_service import get_current_embedding
# from services.embedding_service import get_embedding_history

from flask import flash

from services.embedding_service import (

    use_embedding,

    get_embedding_history,

    get_current_embedding,
    
    get_embedding_metadata,
    
    generate_schema_embeddings,

)
schema_bp = Blueprint(

    "schema",

    __name__,

    url_prefix="/schema"

)

@schema_bp.route("/")
def index():

    schema = load_schema()

    summary = schema_summary()

    embedding = get_current_embedding()

    histories = get_embedding_history()
    current_database = get_current_database()
    return render_template(

        "schema/index.html",

        schema=schema,

        summary=summary,

        embedding=embedding,

        histories=histories,

        embedding_models=Config.EMBEDDING_MODELS,
        current_database=current_database

    )


    
@schema_bp.route(

    "/upload",

    methods=["GET","POST"]

)
def upload():

    if request.method=="POST":

        file = request.files["schema"]

        save_schema(file)
        return redirect(

            url_for("schema.index")

        )

    return render_template(

        "schema/upload.html"

    )
    
@schema_bp.route("/embedding")
def embedding():

    info = get_embedding_metadata()

    return render_template(

        "schema/embedding.html",

        info=info

    )
    
@schema_bp.route(
    "/generate_embedding",
    methods=["POST"]
)
def generate_embedding():

    model = request.form["model"]

    try:

        generate_schema_embeddings(model)

        flash(

            "Schema embedding berhasil dibuat.",

            "success"

        )

    except Exception as e:

        flash(

            str(e),

            "danger"

        )

    return redirect(

        url_for("schema.index")

    )
    
@schema_bp.route("/use_embedding/<version>")
def use_embedding(version):

    from services.embedding_service import use_embedding_version

    use_embedding_version(version)

    flash(

        f"Embedding version {version} digunakan.",

        "success"

    )

    return redirect(

        url_for("schema.index")

    )
    
@schema_bp.route(

    "/embedding/use/<version>"

)

def use_embedding_route(version):

    success = use_embedding(

        version

    )

    if success:

        flash(

            "Embedding berhasil diaktifkan.",

            "success"

        )

    else:

        flash(

            "Embedding tidak ditemukan.",

            "danger"

        )

    return redirect(

        url_for(

            "schema.index"

        )

    )
    
@schema_bp.route(

    "/embedding/delete/<version>"

)

def delete_embedding(version):

    from services.embedding_service import delete_embedding

    try:

        delete_embedding(version)

        flash(

            "Embedding berhasil dihapus.",

            "success"

        )

    except Exception as e:

        flash(

            str(e),

            "danger"

        )

    return redirect(

        url_for(

            "schema.index"

        )

    )
    