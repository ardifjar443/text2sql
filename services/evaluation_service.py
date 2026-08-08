import re
import pymysql

from config import Config


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():
    """
    Membuat koneksi ke database MySQL.
    """

    return pymysql.connect(
        host=Config.DB_HOST,
        port=int(Config.DB_PORT),
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


# ==========================================================
# NORMALIZE SQL
# ==========================================================

import re

def normalize_sql(sql):

    if not sql:
        return ""

    # Lowercase
    sql = sql.lower()

    # Hapus newline dan tab
    sql = sql.replace("\n", " ")
    sql = sql.replace("\t", " ")

    # Rapikan whitespace
    sql = re.sub(r"\s+", " ", sql)

    # Hapus titik koma di akhir
    sql = sql.rstrip(";")

    # Hilangkan spasi di sekitar koma
    sql = re.sub(r"\s*,\s*", ",", sql)

    # Hilangkan spasi setelah (
    sql = re.sub(r"\(\s+", "(", sql)

    # Hilangkan spasi sebelum )
    sql = re.sub(r"\s+\)", ")", sql)

    # Hilangkan spasi di sekitar operator
    sql = re.sub(r"\s*=\s*", "=", sql)
    sql = re.sub(r"\s*>\s*", ">", sql)
    sql = re.sub(r"\s*<\s*", "<", sql)
    sql = re.sub(r"\s*>=\s*", ">=", sql)
    sql = re.sub(r"\s*<=\s*", "<=", sql)
    sql = re.sub(r"\s*!=\s*", "!=", sql)

    return sql.strip()


# ==========================================================
# EXACT MATCH
# ==========================================================

def exact_match(
    generated_sql,
    ground_truth_sql
):
    """
    Menghitung Exact Match.
    """

    generated = normalize_sql(
        generated_sql
    )

    ground_truth = normalize_sql(
        ground_truth_sql
    )

    return generated == ground_truth


# ==========================================================
# EXACT MATCH DETAIL
# ==========================================================

def exact_match_detail(
    generated_sql,
    ground_truth_sql
):
    """
    Mengembalikan detail hasil EM.
    """

    generated = normalize_sql(
        generated_sql
    )

    ground_truth = normalize_sql(
        ground_truth_sql
    )

    return {

        "generated": generated,

        "ground_truth": ground_truth,

        "exact_match": generated == ground_truth

    }


# ==========================================================
# CHECK SQL VALID
# ==========================================================

def validate_sql(sql):
    """
    Validasi sederhana SQL.
    """

    if sql is None:
        return False

    sql = sql.strip()

    if sql == "":
        return False

    keywords = [

        "select",

        "insert",

        "update",

        "delete"

    ]

    return sql.lower().startswith(
        tuple(keywords)
    )


# ==========================================================
# SQL STATISTICS
# ==========================================================

def sql_statistics(sql):
    """
    Statistik sederhana SQL.
    """

    sql = normalize_sql(sql)

    return {

        "characters": len(sql),

        "words": len(sql.split()),

        "lines": len(sql.split("\n"))

    }
    
def execute_sql(sql):
    """
    Menjalankan SQL ke database.
    """

    conn = None

    try:

        conn = get_connection()

        with conn.cursor() as cursor:

            cursor.execute(sql)

            rows = cursor.fetchall()

        return {

            "success": True,

            "rows": rows,

            "count": len(rows),

            "error": None

        }

    except Exception as e:

        return {

            "success": False,

            "rows": [],

            "count": 0,

            "error": str(e)

        }

    finally:

        if conn:

            conn.close()
            
def normalize_result(rows):
    """
    Normalisasi hasil query agar mudah dibandingkan.
    """

    normalized = []

    for row in rows:

        normalized.append(

            tuple(row.values())

        )

    return normalized

import pandas as pd


def compare_result(generated_rows, ground_truth_rows):

    df_generated = pd.DataFrame(generated_rows)
    df_ground = pd.DataFrame(ground_truth_rows)

    # jumlah kolom harus sama
    if df_generated.shape[1] != df_ground.shape[1]:
        return False

    # ubah semua nilai menjadi string
    df_generated = df_generated.astype(str)
    df_ground = df_ground.astype(str)

    # samakan nama kolom sementara
    df_generated.columns = range(df_generated.shape[1])
    df_ground.columns = range(df_ground.shape[1])

    # jumlah baris
    if len(df_generated) != len(df_ground):
        return False

    # urutkan berdasarkan semua kolom
    sort_columns = list(df_ground.columns)

    df_generated = (
        df_generated
        .sort_values(by=sort_columns)
        .reset_index(drop=True)
    )

    df_ground = (
        df_ground
        .sort_values(by=sort_columns)
        .reset_index(drop=True)
    )

    return df_generated.equals(df_ground)

def execution_accuracy(

    generated_sql,

    ground_truth_sql

):

    generated = execute_sql(

        generated_sql

    )

    ground_truth = execute_sql(

        ground_truth_sql

    )

    if not generated["success"]:

        return {

            "execution_accuracy": False,

            "generated_result": [],

            "ground_truth_result": [],

            "generated_error": generated["error"],

            "ground_truth_error": None

        }

    if not ground_truth["success"]:

        return {

            "execution_accuracy": False,

            "generated_result": generated["rows"],

            "ground_truth_result": [],

            "generated_error": None,

            "ground_truth_error": ground_truth["error"]

        }

    ex = compare_result(

        generated["rows"],

        ground_truth["rows"]

    )

    return {

        "execution_accuracy": ex,

        "generated_result": generated["rows"],

        "ground_truth_result": ground_truth["rows"],

        "generated_error": None,

        "ground_truth_error": None

    }
    
def evaluate_sql(

    generated_sql,

    ground_truth_sql

):

    em = exact_match(

        generated_sql,

        ground_truth_sql

    )

    ex = execution_accuracy(

        generated_sql,

        ground_truth_sql

    )

    return {

        "generated_sql": generated_sql,

        "ground_truth_sql": ground_truth_sql,

        "exact_match": em,

        "execution_accuracy": ex["execution_accuracy"],

        "generated_result": ex["generated_result"],

        "ground_truth_result": ex["ground_truth_result"],

        "generated_error": ex["generated_error"],

        "ground_truth_error": ex["ground_truth_error"]

    }
    
import re

def extract_sql(text):
    if text is None:
        return ""

    # hapus markdown ```sql
    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")

    # ambil query mulai SELECT
    match = re.search(
        r"(SELECT[\s\S]*?;?$)",
        text,
        flags=re.IGNORECASE
    )

    if match:
        sql = match.group(1).strip()
    else:
        sql = text.strip()

    # jika ada penjelasan setelah query
    sql = re.split(
        r"\n\s*\n|Perlu diingat|Penjelasan|Explanation|Catatan",
        sql
    )[0]

    sql = sql.strip()

    if not sql.endswith(";"):
        sql += ";"

    return sql