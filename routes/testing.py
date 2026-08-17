from flask import request
from flask import Blueprint
from flask import jsonify
from flask import render_template

from services.testing_service import run_web_testing

testing_bp = Blueprint(
    "testing",
    __name__,
    url_prefix="/testing"
)

@testing_bp.route("/")
def index():
    return render_template(
        "testing/index.html",
    )

@testing_bp.post("/api/text-to-sql")
def text_to_sql():

    try:

        data = request.get_json()

        question = data.get("question")

        if not question:
            return jsonify({
                "success": False,
                "error": "Pertanyaan tidak boleh kosong."
            }), 400

        result = run_web_testing(

            question=question,

            retrieval=data.get(
                "retrieval",
                "adaptive_gap"
            ),

            embedding_model=data.get(
                "embedding_model",
                "google/gemini-embedding-2"
            ),

            llm_model=data.get(
                "llm_model",
                "meta-llama/llama-3.3-70b-instruct"
            ),

            temperature=data.get(
                "temperature",
                0
            ),

            max_token=data.get(
                "max_token",
                512
            )

        )

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500