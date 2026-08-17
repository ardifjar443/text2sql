# testing.py

from services.testing_service import run_testing


def main():

    print("=" * 60)
    print("        NATURAL LANGUAGE TO SQL - TESTING")
    print("=" * 60)

    # ============================================
    # CONFIGURATION
    # ============================================

    retrieval = "adaptive_mean"

    embedding_model = "gemini-embedding-2"

    llm_model = "llama-3.3-70b-instruct"

    temperature = 0

    max_token = 512

    # ============================================
    # INPUT QUESTION
    # ============================================

    print()

    question = input(
        "Masukkan pertanyaan:\n> "
    ).strip()

    if not question:

        print("\nPertanyaan tidak boleh kosong.")

        return

    print()
    print("-" * 60)
    print("Processing...")
    print("-" * 60)

    try:

        # ========================================
        # RUN TESTING
        # ========================================

        result = run_testing(

            question=question,

            retrieval=retrieval,

            embedding_model=embedding_model,

            llm_model=llm_model,

            temperature=temperature,

            max_token=max_token

        )

        # ========================================
        # DISPLAY RESULT
        # ========================================

        print()
        print("=" * 60)
        print("GENERATED SQL")
        print("=" * 60)

        print(result["generated_sql"])

        # ========================================
        # RETRIEVAL INFORMATION
        # ========================================

        print()
        print("=" * 60)
        print("RETRIEVAL INFORMATION")
        print("=" * 60)

        print(
            f"Retrieval : {result['retrieval']}"
        )

        print(
            f"Tables    : {result['table_count']}"
        )

        print(
            f"Columns   : {result['column_count']}"
        )

        # ========================================
        # SELECTED TABLES
        # ========================================

        print()
        print("Selected Tables:")

        if result["selected_tables"]:

            for table in result["selected_tables"]:

                print(f"  - {table}")

        else:

            print("  - Full Schema")

        # ========================================
        # SELECTED COLUMNS
        # ========================================

        print()
        print("Selected Columns:")

        if result["selected_columns"]:

            for column in result["selected_columns"]:

                print(f"  - {column}")

        else:

            print("  - Full Schema")

        # ========================================
        # LLM STATISTICS
        # ========================================

        print()
        print("=" * 60)
        print("LLM STATISTICS")
        print("=" * 60)

        statistics = result["llm_statistics"]

        print(
            f"Prompt Tokens     : "
            f"{statistics['prompt_tokens']}"
        )

        print(
            f"Completion Tokens : "
            f"{statistics['completion_tokens']}"
        )

        print(
            f"Total Tokens      : "
            f"{statistics['total_tokens']}"
        )

        print(
            f"LLM Latency       : "
            f"{statistics['latency']:.4f} s"
        )

        # ========================================
        # PIPELINE TIMING
        # ========================================

        print()
        print("=" * 60)
        print("PIPELINE TIMING")
        print("=" * 60)

        timing = result["timing"]

        print(
            f"Retrieval Time    : "
            f"{timing['retrieval_time']:.4f} s"
        )

        print(
            f"Prompt Build Time : "
            f"{timing['prompt_build_time']:.4f} s"
        )

        print(
            f"LLM Generation    : "
            f"{timing['llm_generation_time']:.4f} s"
        )

        print(
            f"Total Pipeline    : "
            f"{timing['total_pipeline_time']:.4f} s"
        )

        print()
        print("=" * 60)
        print("TESTING SELESAI")
        print("=" * 60)

    except Exception as e:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)

        print(str(e))


if __name__ == "__main__":

    main()