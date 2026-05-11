import pandas as pd

from config import (
    AUTHORS_DIR,
    RANDOM_SEED,
    TEXT_COLUMN,
    TRAIN_SIZE,
)

from data.loader import (
    load_author_csv
)

from data.splitter import (
    split_dataset
)

from features.graphematic_extractor import (
    extract_graphematic_features
)

from models.heuristic_similarity import (
    build_heuristic_profile,
    heuristic_similarity
)

from utils.io import (
    save_graphematic_negative_results,
    save_graphematic_profile,
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
        "pipeline": "graphematic_negative",
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
        "compared_messages_count": len(
            results_df
        )
    }


def verify_graphematic_negative_author(
        profile_author,
        compared_author
):
    print(
        f"\n========== GRAPHEMATIC NEGATIVE: "
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

    profile = build_heuristic_profile(
        train_df=train_df,
        extract_features=extract_graphematic_features
    )

    save_graphematic_profile(
        profile,
        profile_author
    )

    results = []

    for idx, row in (
            compared_df.iterrows()
    ):
        text = row[
            TEXT_COLUMN
        ]

        features = extract_graphematic_features(
            text
        )

        score = heuristic_similarity(
            features=features,
            profile=profile
        )

        result = {
            "profile_author": profile_author,
            "compared_author": compared_author,
            "comparison_type": "negative",
            "message_id": idx,
            "similarity_percent": score,
            "text": text
        }

        result.update(
            features
        )

        results.append(
            result
        )

    results_df = pd.DataFrame(
        results
    )

    if results_df.empty:
        raise ValueError(
            f"No compared messages were created for "
            f"{compared_author}"
        )

    save_graphematic_negative_results(
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
        f"Graphematic negative mean similarity: "
        f"{summary['mean_similarity']}%"
    )

    return summary
