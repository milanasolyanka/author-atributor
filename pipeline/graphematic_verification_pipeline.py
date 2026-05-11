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
    save_graphematic_profile,
    save_graphematic_results,
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
        author_name,
        results_df
):
    similarity = results_df[
        "similarity_percent"
    ]

    return {
        "author": author_name,
        "pipeline": "graphematic",
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
        "test_messages_count": len(
            results_df
        )
    }


def verify_graphematic_author(
        author_name
):
    print(
        f"\n========== GRAPHEMATIC: "
        f"{author_name} "
        f"=========="
    )

    df = _load_author(
        author_name
    )

    print(
        f"[{author_name}] "
        f"Messages loaded: "
        f"{len(df)}"
    )

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

    profile = build_heuristic_profile(
        train_df=train_df,
        extract_features=extract_graphematic_features
    )

    save_graphematic_profile(
        profile,
        author_name
    )

    results = []

    for idx, row in (
            test_df.iterrows()
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
            "author": author_name,
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
            f"No test messages were created for "
            f"{author_name}"
        )

    save_graphematic_results(
        results_df,
        author_name
    )

    summary = _build_summary(
        author_name,
        results_df
    )

    print(
        f"[{author_name}] "
        f"Graphematic mean similarity: "
        f"{summary['mean_similarity']}%"
    )

    return summary
