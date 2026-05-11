import pandas as pd

from config import (
    AUTHORS_DIR,
    RANDOM_SEED,
    TEXT_COLUMN,
    TRAIN_SIZE,
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
    FEATURE_WEIGHTS,
    weighted_z_similarity
)

from utils.io import (
    save_negative_results,
    save_train_test
)


def _load_author(author_name):
    csv_path = (
        f"{AUTHORS_DIR}/"
        f"{author_name}.csv"
    )

    return load_author_csv(
        csv_path
    )


def _build_summary(
        profile_author,
        compared_author,
        results_df
):
    similarity = results_df[
        "similarity_percent"
    ]

    return {
        "profile_author": profile_author,
        "compared_author": compared_author,
        "comparison_type": "negative",
        "mean_similarity": round(
            similarity.mean(),
            2
        ),
        "std_similarity": round(
            similarity.std(),
            2
        ),
        "min_similarity": round(
            similarity.min(),
            2
        ),
        "max_similarity": round(
            similarity.max(),
            2
        ),
        "windows_count": len(
            results_df
        )
    }


def verify_negative_author(
        profile_author,
        compared_author
):
    """
    Negative verification:
    build a profile from author A train data and compare it
    with windows from author B texts.
    """

    print(
        f"\n========== NEGATIVE: "
        f"{profile_author} vs {compared_author} "
        f"=========="
    )

    if profile_author == compared_author:
        raise ValueError(
            "For negative comparison profile_author "
            "and compared_author must be different"
        )

    profile_df = _load_author(
        profile_author
    )

    compared_df = _load_author(
        compared_author
    )

    print(
        f"[{profile_author}] "
        f"Profile messages loaded: "
        f"{len(profile_df)}"
    )

    print(
        f"[{compared_author}] "
        f"Compared messages loaded: "
        f"{len(compared_df)}"
    )

    train_df, test_df = (
        split_dataset(
            df=profile_df,
            train_size=TRAIN_SIZE,
            random_seed=RANDOM_SEED
        )
    )

    save_train_test(
        train_df,
        test_df,
        profile_author
    )

    means, stds = (
        build_author_profile(
            train_df
        )
    )

    print(
        f"[{profile_author}] "
        f"Author profile built"
    )

    results = []

    for idx, row in (
            compared_df.iterrows()
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

            if not features:
                continue

            score = (
                weighted_z_similarity(
                    features=features,
                    means=means,
                    stds=stds,
                    weights=FEATURE_WEIGHTS
                )
            )

            results.append({
                "profile_author": profile_author,
                "compared_author": compared_author,
                "comparison_type": "negative",
                "message_id": idx,
                "window_id": window_id,
                "window_length": len(window),
                "similarity_percent": score,
                "text": window
            })

    results_df = pd.DataFrame(
        results
    )

    if results_df.empty:
        raise ValueError(
            f"No windows were created for "
            f"{compared_author}"
        )

    save_negative_results(
        results_df,
        profile_author,
        compared_author
    )

    summary = _build_summary(
        profile_author,
        compared_author,
        results_df
    )

    print(
        f"[{profile_author} vs {compared_author}] "
        f"Mean negative similarity: "
        f"{summary['mean_similarity']}%"
    )

    return summary
