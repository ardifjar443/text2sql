import os
import json
import pandas as pd


# ============================================================
# KONFIGURASI
# ============================================================

# Folder tempat file-file JSON berada
FOLDER_JSON = "./data/raw/dataset_lain"

# Nama file Excel hasil
OUTPUT_EXCEL = "dataset_text_to_sql.xlsx"


# ============================================================
# PROSES
# ============================================================

data_excel = []

# Ambil semua file JSON dalam folder
for filename in os.listdir(FOLDER_JSON):

    if not filename.lower().endswith(".json"):
        continue

    filepath = os.path.join(FOLDER_JSON, filename)

    print(f"Membaca: {filename}")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Struktur JSON:
        # {
        #   "RES-S6-01": {...},
        #   "RES-S6-02": {...}
        # }

        for item_id, item in data.items():

            data_excel.append({
                "pertanyaan": item.get("question_id", ""),
                "category": item.get("category", ""),
                "db": item.get("db", ""),
                "solution_sql": item.get("solution_sql", "")
            })

    except Exception as e:
        print(f"Gagal membaca {filename}: {e}")


# ============================================================
# BUAT DATAFRAME
# ============================================================

df = pd.DataFrame(
    data_excel,
    columns=[
        "pertanyaan",
        "category",
        "db",
        "solution_sql"
    ]
)


# ============================================================
# EXPORT KE EXCEL
# ============================================================

df.to_excel(
    OUTPUT_EXCEL,
    index=False,
    engine="openpyxl"
)


print("\n========================================")
print("Proses selesai!")
print(f"Total data : {len(df)}")
print(f"File Excel : {OUTPUT_EXCEL}")
print("========================================")