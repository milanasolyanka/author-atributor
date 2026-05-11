import numpy as np
import pandas as pd

from config import (
    AUTHORS_DIR,
    TEXT_COLUMN,
    TRAIN_SIZE,
    RANDOM_SEED,
    WINDOW_SIZE,
    WINDOW_STEP,
)

from data.loader import (
    load_author_csv
)

from data.splitter import (
    split_dataset
)

from features.feature_extractor import (
    extract_features
)

from features.windows import (
    create_windows
)

from models.author_profile import (
    build_author_profile
)

from models.weighted_zscore import (
    weighted_z_similarity,
    FEATURE_WEIGHTS
)

from utils.io import (
    save_results,
    save_train_test
)


def verify_author(
        author_name
):
    """
    Полный pipeline
    верификации автора.
    """

    print(
        f"\n========== "
        f"{author_name} "
        f"=========="
    )

    csv_path = (
        f"{AUTHORS_DIR}/"
        f"{author_name}.csv"
    )

    # =====================
    # Load dataset
    # =====================

    df = load_author_csv(
        csv_path
    )

    print(
        f"[{author_name}] "
        f"Messages loaded: "
        f"{len(df)}"
    )

    # =====================
    # Train/Test split
    # =====================

    train_df, test_df = (
        split_dataset(
            df=df,
            train_size=TRAIN_SIZE,
            random_seed=RANDOM_SEED
        )
    )

    save_train_test(
        train_df,
        test_df,
        author_name
    )

    # =====================
    # Author profile
    # =====================

    means, stds = (
        build_author_profile(
            train_df
        )
    )

    print(
        f"[{author_name}] "
        f"Author profile built"
    )

    # =====================
    # Verification
    # =====================

    results = []

    for idx, row in (
            test_df.iterrows()
    ):
        text = row[
            TEXT_COLUMN
        ]

        windows = (
            create_windows(
                text=text,
                window_size=WINDOW_SIZE,
                step=WINDOW_STEP
            )
        )

        for window_id, window in enumerate(
                windows
        ):
            features = (
                extract_features(
                    window
                )
            )

            score = (
                weighted_z_similarity(
                    features=features,
                    means=means,
                    stds=stds,
                    weights=FEATURE_WEIGHTS
                )
            )

            results.append({
                "author": author_name,
                "message_id": idx,
                "window_id": window_id,
                "window_length": len(window),
                "similarity_percent": score,
                "text": window
            })

    results_df = pd.DataFrame(
        results
    )

    save_results(
        results_df,
        author_name
    )

    # =====================
    # Summary
    # =====================

    mean_similarity = (
        results_df[
            "similarity_percent"
        ].mean()
    )

    std_similarity = (
        results_df[
            "similarity_percent"
        ].std()
    )

    min_similarity = (
        results_df[
            "similarity_percent"
        ].min()
    )

    max_similarity = (
        results_df[
            "similarity_percent"
        ].max()
    )

    windows_count = len(
        results_df
    )

    summary = {
        "author": author_name,
        "mean_similarity": round(
            mean_similarity,
            2
        ),
        "std_similarity": round(
            std_similarity,
            2
        ),
        "min_similarity": round(
            min_similarity,
            2
        ),
        "max_similarity": round(
            max_similarity,
            2
        ),
        "windows_count": windows_count
    }

    print(
        f"[{author_name}] "
        f"Mean similarity: "
        f"{summary['mean_similarity']}%"
    )

    return summary