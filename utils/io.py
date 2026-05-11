from pathlib import Path

import pandas as pd

from config import RESULTS_DIR


def get_author_output_dir(author_name):
    """
    Создает папку результатов автора.

    results/
        author_name/
    """
    output_dir = (
        Path(RESULTS_DIR)
        / author_name
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_dir


def save_train_test(
        train_df,
        test_df,
        author_name
):
    """
    Сохраняет train/test выборки.
    """

    output_dir = get_author_output_dir(
        author_name
    )

    train_path = (
        output_dir
        / "train.csv"
    )

    test_path = (
        output_dir
        / "test.csv"
    )

    train_df.to_csv(
        train_path,
        index=False,
        encoding="utf-8-sig"
    )

    test_df.to_csv(
        test_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"[{author_name}] "
        f"Train saved → {train_path}"
    )

    print(
        f"[{author_name}] "
        f"Test saved → {test_path}"
    )


def save_results(
        results_df,
        author_name
):
    """
    Сохраняет verification_results.csv
    """

    output_dir = get_author_output_dir(
        author_name
    )

    results_path = (
        output_dir
        / "verification_results.csv"
    )

    results_df.to_csv(
        results_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"[{author_name}] "
        f"Results saved → {results_path}"
    )


def save_negative_results(
        results_df,
        profile_author,
        compared_author
):
    output_dir = (
        get_author_output_dir(
            profile_author
        )
        / "negative"
        / compared_author
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    results_path = (
        output_dir
        / "negative_verification_results.csv"
    )

    results_df.to_csv(
        results_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"[{profile_author} vs {compared_author}] "
        f"Negative results saved -> {results_path}"
    )


def save_graphematic_profile(
        profile,
        author_name
):
    output_dir = (
        Path(RESULTS_DIR)
        / "graphematic_profiles"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    profile_path = (
        output_dir
        / f"{author_name}_profile.csv"
    )

    profile_df = pd.DataFrame([
        profile
    ])

    profile_df.insert(
        0,
        "author",
        author_name
    )

    profile_df.to_csv(
        profile_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"[{author_name}] "
        f"Graphematic profile saved -> {profile_path}"
    )


def save_graphematic_results(
        results_df,
        author_name
):
    output_dir = (
        get_author_output_dir(
            author_name
        )
        / "graphematic"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    results_path = (
        output_dir
        / "graphematic_verification_results.csv"
    )

    results_df.to_csv(
        results_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"[{author_name}] "
        f"Graphematic results saved -> {results_path}"
    )


def save_graphematic_negative_results(
        results_df,
        profile_author,
        compared_author
):
    output_dir = (
        get_author_output_dir(
            profile_author
        )
        / "graphematic_negative"
        / compared_author
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    results_path = (
        output_dir
        / "graphematic_negative_results.csv"
    )

    results_df.to_csv(
        results_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"[{profile_author} vs {compared_author}] "
        f"Graphematic negative results saved -> {results_path}"
    )


def save_summary(
        summary_df
):
    """
    Сохраняет global_summary.csv
    """

    output_dir = Path(
        RESULTS_DIR
    )

    output_dir.mkdir(
        exist_ok=True
    )

    summary_path = (
        output_dir
        / "global_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Global summary saved → "
        f"{summary_path}"
    )


def save_negative_summary(
        summary_df
):
    output_dir = Path(
        RESULTS_DIR
    )

    output_dir.mkdir(
        exist_ok=True
    )

    summary_path = (
        output_dir
        / "negative_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Negative summary saved -> "
        f"{summary_path}"
    )


def save_graphematic_summary(
        summary_df
):
    output_dir = Path(
        RESULTS_DIR
    )

    output_dir.mkdir(
        exist_ok=True
    )

    summary_path = (
        output_dir
        / "graphematic_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Graphematic summary saved -> "
        f"{summary_path}"
    )


def save_graphematic_negative_summary(
        summary_df
):
    output_dir = Path(
        RESULTS_DIR
    )

    output_dir.mkdir(
        exist_ok=True
    )

    summary_path = (
        output_dir
        / "graphematic_negative_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Graphematic negative summary saved -> "
        f"{summary_path}"
    )
