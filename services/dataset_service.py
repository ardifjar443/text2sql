from pathlib import Path
from datetime import datetime
import pandas as pd
import json
import shutil

# ==========================================================
# PATH
# ==========================================================

DATASET_ROOT = Path("data/dataset")

CURRENT_DIR = DATASET_ROOT / "current"
HISTORY_DIR = DATASET_ROOT / "history"

CURRENT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATASET_FILE = CURRENT_DIR / "dataset.xlsx"
METADATA_FILE = CURRENT_DIR / "metadata.json"


# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    if not DATASET_FILE.exists():

        return pd.DataFrame()

    return pd.read_excel(DATASET_FILE)


# ==========================================================
# SAVE DATASET
# ==========================================================

def save_dataset(df):

    df.to_excel(
        DATASET_FILE,
        index=False
    )

    metadata = create_metadata(
        DATASET_FILE,
        df
    )

    with open(
        METADATA_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# UPLOAD DATASET
# ==========================================================

def save_uploaded_dataset(file):

    temp = CURRENT_DIR / "temp.xlsx"

    file.save(temp)

    df = pd.read_excel(temp)

    required = [

        "ID",

        "Question",

        "SQL",

        "Level"

    ]

    for column in required:

        if column not in df.columns:

            temp.unlink()

            raise Exception(

                f"Kolom '{column}' tidak ditemukan."

            )

    if DATASET_FILE.exists():

        timestamp = datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        history = HISTORY_DIR / timestamp

        history.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(

            DATASET_FILE,

            history / "dataset.xlsx"

        )

        if METADATA_FILE.exists():

            shutil.copy2(

                METADATA_FILE,

                history / "metadata.json"

            )

    temp.replace(DATASET_FILE)

    metadata = create_metadata(

        DATASET_FILE,

        df

    )

    with open(

        METADATA_FILE,

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            metadata,

            f,

            indent=4,

            ensure_ascii=False

        )


# ==========================================================
# CREATE METADATA
# ==========================================================

def create_metadata(

    dataset_file,

    dataframe

):

    return {

        "dataset_name":

            dataset_file.name,

        "question_count":

            len(dataframe),

        "created_at":

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            ),

        "generator":

            "Text2SQL Studio",

        "version":

            datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            ),

        "columns":

            dataframe.columns.tolist()

    }


# ==========================================================
# CURRENT DATASET
# ==========================================================

def get_dataset_metadata():

    if not METADATA_FILE.exists():

        return None

    with open(

        METADATA_FILE,

        encoding="utf8"

    ) as f:

        return json.load(f)


# ==========================================================
# DATASET HISTORY
# ==========================================================

def get_dataset_history():

    histories = []

    if not HISTORY_DIR.exists():

        return histories

    folders = sorted(

        HISTORY_DIR.iterdir(),

        reverse=True

    )

    current = get_dataset_metadata()

    current_version = None

    if current:

        current_version = current.get(

            "version"

        )

    for folder in folders:

        metadata = folder / "metadata.json"

        if not metadata.exists():

            continue

        with open(

            metadata,

            encoding="utf8"

        ) as f:

            info = json.load(f)

        histories.append({

            "version":

                info.get(

                    "version"

                ),

            "dataset_name":

                info.get(

                    "dataset_name"

                ),

            "question_count":

                info.get(

                    "question_count"

                ),

            "created_at":

                info.get(

                    "created_at"

                ),

            "is_active":

                info.get(

                    "version"

                ) == current_version

        })

    return histories

# ==========================================================
# GET GROUND TRUTH SQL
# ==========================================================

def get_ground_truth_sql(question):
    """
    Mengambil SQL ground truth berdasarkan pertanyaan.
    """

    dataset = load_dataset()

    if dataset.empty:
        return None

    # Pastikan kolom ada
    if "Question" not in dataset.columns:
        raise Exception("Kolom 'Question' tidak ditemukan pada dataset.")

    if "SQL" not in dataset.columns:
        raise Exception("Kolom 'SQL Ground Truth' tidak ditemukan pada dataset.")

    row = dataset[
        dataset["Question"].astype(str).str.strip()
        ==
        question.strip()
    ]

    if row.empty:
        return None

    return row.iloc[0]["SQL"]