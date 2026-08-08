import json
from pathlib import Path

import pandas as pd

BATCH_DIR = Path("data/experiment/history/batch")

rows = []

for folder in sorted(BATCH_DIR.iterdir()):

    if not folder.is_dir():
        continue

    summary_file = folder / "summary.json"

    if not summary_file.exists():
        continue

    with open(summary_file, "r", encoding="utf8") as f:
        summary = json.load(f)

    rows.append({

        "Experiment": folder.name,

        "LLM Model":
            summary.get("model llm ", ""),

        "Embedding":
            summary.get("embedding model", ""),

        "Retrieval":
            summary.get("retrieval", ""),

        "Question":
            summary.get("total_question", 0),

        "Exact Match":
            summary.get("exact_match", 0),

        "Execution":
            summary.get("execution_accuracy", 0),

        "EM (%)":
            summary.get("exact_match_percentage", 0),

        "EX (%)":
            summary.get("execution_accuracy_percentage", 0),

        "Latency (s)":
            summary.get("average_latency", 0),

        "Prompt Token":
            summary.get("average_prompt_tokens", 0),

        "Completion Token":
            summary.get("average_completion_tokens", 0),

        "Total Token":
            summary.get("average_total_tokens", 0),

        "Created":
            summary.get("created_at", "")

    })

df = pd.DataFrame(rows)

df = df.sort_values(
    by="Created",
    ascending=False
)

output_excel = BATCH_DIR / "summary_experiment.xlsx"

df.to_excel(
    output_excel,
    index=False
)

print(df)

print()

print("Saved to:", output_excel)