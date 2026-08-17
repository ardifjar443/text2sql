from services.batch_experiment_service import run_batch

MODELS = [
    # "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.2-3b-instruct",
    "meta-llama/llama-3.2-1b-instruct",
    # "google/gemini-3.5-flash-lite"
    # "meta-llama/llama-3.3-70b-instruct"
]

RETRIEVALS = [
    "full",
    # "top3",
    # "top5",
    # "top7",
    # "adaptive_mean",
    # "adaptive_gap",
    # "adaptive_percentile75"
]

EMBEDDING_MODEL = "google/gemini-embedding-2"

TEMPERATURE = 0
MAX_TOKEN = 1024


for model in MODELS:

    print("=" * 80)
    print(f"MODEL : {model}")
    print("=" * 80)

    for retrieval in RETRIEVALS:

        print(f"\nRetrieval : {retrieval}")

        try:

            result = run_batch(
                retrieval=retrieval,
                embedding_model=EMBEDDING_MODEL,
                llm_model=model,
                temperature=TEMPERATURE,
                max_token=MAX_TOKEN
            )

            summary = result["summary"]

            print(
                f"EM : {summary['exact_match']} "
                f"({summary['exact_match_percentage']}%)"
            )

            print(
                f"EX : {summary['execution_accuracy']} "
                f"({summary['execution_accuracy_percentage']}%)"
            )

            print(
                f"Latency : {summary['average_latency']} s"
            )

            print(
                f"History : {result['history']}"
            )

        except Exception as e:

            print(f"ERROR : {e}")

print("\nSemua eksperimen selesai.")