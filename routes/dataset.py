from flask import Blueprint, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from services.dataset_service import (
    load_dataset,
    save_dataset,
    save_uploaded_dataset,
    get_dataset_metadata,
    get_dataset_history
)

print("Dataset Blueprint Loaded")

dataset_bp = Blueprint(
    "dataset",
    __name__,
    url_prefix="/dataset"
)

@dataset_bp.route("/")
def index():

    dataset = load_dataset()

    metadata = get_dataset_metadata()

    histories = get_dataset_history()

    return render_template(

        "dataset/index.html",

        dataset=dataset,

        metadata=metadata,

        histories=histories

    )
    
@dataset_bp.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    if request.method == "POST":

        file = request.files.get("dataset")

        if file:

            save_uploaded_dataset(file)

        return redirect(
            url_for("dataset.index")
        )

    return render_template(
        "dataset/upload.html"
    )
    
@dataset_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        df = load_dataset()

        question_id = request.form["id"].strip()

        # Cek ID sudah ada atau belum
        if question_id in df["ID"].astype(str).values:

            flash("ID sudah digunakan.", "danger")

            return redirect(
                url_for("dataset.add")
            )

        new_row = {

            "ID": question_id,

            "Question": request.form["question"],

            "SQL": request.form["sql"],

            "Level": request.form["level"]

        }

        df.loc[len(df)] = new_row

        save_dataset(df)

        flash(
            "Data berhasil ditambahkan.",
            "success"
        )

        return redirect(
            url_for("dataset.index")
        )

    return render_template(
        "dataset/form.html",
        action="Tambah",
        data=None
    )
    
@dataset_bp.route("/edit/<question_id>", methods=["GET", "POST"])
def edit(question_id):

    df = load_dataset()

    row = df[
        df["ID"].astype(str) == str(question_id)
    ]

    if row.empty:

        flash(
            "Data tidak ditemukan.",
            "danger"
        )

        return redirect(
            url_for("dataset.index")
        )

    if request.method == "POST":

        idx = row.index[0]

        df.at[idx, "Question"] = request.form["question"]

        df.at[idx, "SQL"] = request.form["sql"]

        df.at[idx, "Level"] = request.form["level"]

        save_dataset(df)

        flash(
            "Data berhasil diubah.",
            "success"
        )

        return redirect(
            url_for("dataset.index")
        )

    return render_template(

        "dataset/form.html",

        action="Edit",

        data = row.iloc[0].to_dict()

    )
    
@dataset_bp.route("/delete/<question_id>")
def delete(question_id):

    df = load_dataset()

    before = len(df)

    df = df[
        df["ID"].astype(str) != str(question_id)
    ]

    if len(df) == before:

        flash(
            "Data tidak ditemukan.",
            "danger"
        )

    else:

        save_dataset(df)

        flash(
            "Data berhasil dihapus.",
            "success"
        )

    return redirect(
        url_for("dataset.index")
    )