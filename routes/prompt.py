from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from services.prompt_service import (
    load_prompt,
    save_prompt,
    get_prompt_metadata,
    get_prompt_versions
)

prompt_bp = Blueprint(
    "prompt",
    __name__,
    url_prefix="/prompt"
)


@prompt_bp.route("/")
def index():

    prompt = load_prompt()

    metadata = get_prompt_metadata()

    versions = get_prompt_versions()

    return render_template(

        "prompt/index.html",

        prompt=prompt,

        metadata=metadata,

        versions=versions

    )


@prompt_bp.route(
    "/save",
    methods=["POST"]
)
def save():

    prompt_text = request.form.get(
        "prompt",
        ""
    )

    try:

        save_prompt(
            prompt_text
        )

        flash(

            "Prompt berhasil disimpan.",

            "success"

        )

    except Exception as e:

        flash(

            str(e),

            "danger"

        )

    return redirect(

        url_for(
            "prompt.index"
        )

    )