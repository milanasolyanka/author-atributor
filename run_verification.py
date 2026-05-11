import random

import numpy as np
import pandas as pd

from config import (
    RANDOM_SEED,
    VERIFY_ALL_AUTHORS,
    AUTHOR_NAME
)

from selected_authors import (
    selected_authors
)

from pipeline.verification_pipeline import (
    verify_author
)

from utils.io import (
    save_summary
)


def main():
    random.seed(
        RANDOM_SEED
    )

    np.random.seed(
        RANDOM_SEED
    )

    summaries = []

    # =====================
    # Single author
    # =====================

    if not VERIFY_ALL_AUTHORS:

        summary = verify_author(
            AUTHOR_NAME
        )

        summaries.append(
            summary
        )

    # =====================
    # Multiple authors
    # =====================

    else:
        print(
            "\nRunning "
            "verification for "
            "selected authors..."
        )

        for author in (
                selected_authors
        ):
            try:
                summary = (
                    verify_author(
                        author
                    )
                )

                summaries.append(
                    summary
                )

            except Exception as e:
                print(
                    f"[{author}] "
                    f"FAILED → {e}"
                )

    # =====================
    # Global statistics
    # =====================

    summary_df = pd.DataFrame(
        summaries
    )

    save_summary(
        summary_df
    )

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
        "GLOBAL MEAN "
        f"SIMILARITY: "
        f"{overall_mean}%"
    )

    print(
        "=================="
    )


if __name__ == "__main__":
    main()