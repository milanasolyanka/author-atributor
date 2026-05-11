import random

import pandas as pd

from config import (
    AUTHOR_NAME,
    GRAPHEMATIC_NEGATIVE_COMPARE_ALL_AUTHORS,
    RANDOM_SEED
)

from pipeline.graphematic_negative_pipeline import (
    verify_graphematic_negative_author
)

from selected_authors import (
    selected_authors
)

from utils.io import (
    save_graphematic_negative_summary
)


COMPARED_AUTHOR_NAME = "Саша_Электросталь"


def main():
    random.seed(
        RANDOM_SEED
    )

    summaries = []

    if GRAPHEMATIC_NEGATIVE_COMPARE_ALL_AUTHORS:
        compared_authors = [
            author
            for author in selected_authors
            if author != AUTHOR_NAME
        ]

        print(
            "\nRunning graphematic negative verification "
            f"for {AUTHOR_NAME} against selected authors..."
        )

    else:
        compared_authors = [
            COMPARED_AUTHOR_NAME
        ]

    for compared_author in compared_authors:
        try:
            summary = verify_graphematic_negative_author(
                profile_author=AUTHOR_NAME,
                compared_author=compared_author
            )

            summaries.append(
                summary
            )

        except Exception as e:
            print(
                f"[{AUTHOR_NAME} vs {compared_author}] "
                f"FAILED -> {e}"
            )

    summary_df = pd.DataFrame(
        summaries
    )

    save_graphematic_negative_summary(
        summary_df
    )

    if summary_df.empty:
        print(
            "\nNo graphematic negative summaries were created."
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
        "GRAPHEMATIC NEGATIVE GLOBAL "
        f"MEAN SIMILARITY: "
        f"{overall_mean}%"
    )

    print(
        "=================="
    )


if __name__ == "__main__":
    main()
