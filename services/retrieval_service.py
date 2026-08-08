import numpy as np


def apply_strategy(similarities, strategy, top_k=5):

    similarities.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    strategy = strategy.lower()

    # -------------------------
    # TOP K
    # -------------------------

    if strategy.startswith("top"):

        try:

            k = int(

                strategy.replace(
                    "top",
                    ""
                )

            )

        except:

            k = top_k

        return similarities[:k]

    # -------------------------
    # GAP
    # -------------------------

    elif strategy == "adaptive_gap":

        if len(similarities) <= 1:

            return similarities

        gaps = []

        for i in range(len(similarities)-1):

            gaps.append(

                similarities[i]["similarity"]

                -

                similarities[i+1]["similarity"]

            )

        split = gaps.index(max(gaps))

        return similarities[:split+1]

    # -------------------------
    # MEAN
    # -------------------------

    elif strategy == "adaptive_mean":

        threshold = np.mean(

            [

                s["similarity"]

                for s in similarities

            ]

        )

        return [

            s

            for s in similarities

            if s["similarity"] >= threshold

        ]

    # -------------------------
    # MEAN + SD
    # -------------------------

    elif strategy == "adaptive_mean_sd1":

        values = np.array(

            [

                s["similarity"]

                for s in similarities

            ]

        )

        threshold = values.mean() + values.std()

        return [

            s

            for s in similarities

            if s["similarity"] >= threshold

        ]

    # -------------------------
    # PERCENTILE
    # -------------------------

    elif strategy == "adaptive_percentile75":

        threshold = np.percentile(

            [

                s["similarity"]

                for s in similarities

            ],

            75

        )

        return [

            s

            for s in similarities

            if s["similarity"] >= threshold

        ]

    else:

        raise Exception(

            f"Unknown retrieval strategy : {strategy}"

        )