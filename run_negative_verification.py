import random

import numpy as np
import pandas as pd

from config import (
    AUTHOR_NAME,
    RANDOM_SEED
)

from pipeline.negative_verification_pipeline import (
    verify_negative_author
)

from utils.io import (
    save_negative_summary
)


COMPARED_AUTHOR_NAME = "Sedrik_Ey"


def main():
    random.seed(
        RANDOM_SEED
    )

    np.random.seed(
        RANDOM_SEED
    )

    summary = verify_negative_author(
        profile_author=AUTHOR_NAME,
        compared_author=COMPARED_AUTHOR_NAME
    )

    summary_df = pd.DataFrame([
        summary
    ])

    save_negative_summary(
        summary_df
    )

    print(
        "\n=================="
    )

    print(
        "NEGATIVE MEAN "
        f"SIMILARITY: "
        f"{summary['mean_similarity']}%"
    )

    print(
        "=================="
    )


if __name__ == "__main__":
    main()
