import random

import pandas as pd

from config import (
    AUTHOR_NAME,
    GRAPHEMATIC_VERIFY_ALL_AUTHORS,
    RANDOM_SEED
)

from pipeline.graphematic_verification_pipeline import (
    verify_graphematic_author
)

from selected_authors import (
    selected_authors
)

from utils.io import (
    save_graphematic_summary
)


def main():
    random.seed(
        RANDOM_SEED
    )

    summaries = []

    if GRAPHEMATIC_VERIFY_ALL_AUTHORS:
        print(
            "\nRunning graphematic verification "
            "for selected authors..."
        )

        authors = selected_authors

    else:
        authors = [
            AUTHOR_NAME
        ]

    for author in authors:
        try:
            summary = verify_graphematic_author(
                author
            )

            summaries.append(
                summary
            )

        except Exception as e:
            print(
                f"[{author}] "
                f"FAILED -> {e}"
            )

    summary_df = pd.DataFrame(
        summaries
    )

    save_graphematic_summary(
        summary_df
    )

    if summary_df.empty:
        print(
            "\nNo graphematic summaries were created."
        )

        return

    overall_mean = round(
        summary_df[
            "mean_similarity"
        ].mean(),
        2
    )

    print(
        "\n=================="
    )

    print(
        "GRAPHEMATIC GLOBAL "
        f"MEAN SIMILARITY: "
        f"{overall_mean}%"
    )

    print(
        "=================="
    )


if __name__ == "__main__":
    main()
