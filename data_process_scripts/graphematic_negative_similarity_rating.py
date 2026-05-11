import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


RESULTS_DIR = "results"
INPUT_FILENAME = "graphematic_negative_summary.csv"
OUTPUT_FILENAME = "graphematic_negative_similarity_chart.png"

FIGURE_SIZE = (16, 9)
CHART_COLOR = 'hotpink'
EDGE_COLOR = 'darkred'
LINE_WIDTH = 1
DPI = 300

MAX_NAME_LENGTH = 16
ROTATION_ANGLE = 45
VALUE_OFFSET = 1.0
VALUE_FONTSIZE = 9  # Увеличил для лучшей читаемости
VALUE_FONTWEIGHT = "bold"
GRID_ALPHA = 0.3
GRID_LINESTYLE = "--"

SHOW_STATISTICS = True
SHOW_TABLE = True
SHOW_PLOT = True


def get_project_dir():
    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    return os.path.dirname(
        current_dir
    )


PROJECT_DIR = get_project_dir()

if PROJECT_DIR not in sys.path:
    sys.path.insert(
        0,
        PROJECT_DIR
    )

from config import AUTHOR_NAME  # noqa: E402


TITLE_TEXT = (
    "Graphematic negative mean similarity\n"
    f"profile author: {AUTHOR_NAME}"
)

X_LABEL = "Compared authors"
Y_LABEL = "Mean similarity, %"


def truncate_name(
        name,
        max_length=MAX_NAME_LENGTH
):
    if len(name) > max_length:
        return (
            name[:max_length - 3]
            + "..."
        )

    return name


def get_file_path():
    return os.path.join(
        PROJECT_DIR,
        RESULTS_DIR,
        INPUT_FILENAME
    )


def get_output_path():
    return os.path.join(
        PROJECT_DIR,
        OUTPUT_FILENAME
    )


def load_data(
        file_path
):
    if not os.path.exists(
            file_path
    ):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_csv(
        file_path
    )


def prepare_data(
        df
):
    df_sorted = df.sort_values(
        "mean_similarity",
        ascending=False
    )

    authors_full = df_sorted[
        "compared_author"
    ].tolist()

    authors_short = [
        truncate_name(
            author
        )
        for author in authors_full
    ]

    mean_similarities = df_sorted[
        "mean_similarity"
    ].tolist()

    return (
        df_sorted,
        authors_full,
        authors_short,
        mean_similarities
    )


def create_chart(
        authors_short,
        authors_full,
        mean_similarities
):
    plt.figure(
        figsize=FIGURE_SIZE
    )

    bars = plt.bar(
        authors_short,
        mean_similarities,
        color=CHART_COLOR,
        edgecolor=EDGE_COLOR,
        linewidth=LINE_WIDTH
    )

    plt.title(
        TITLE_TEXT,
        fontsize=14,
        fontweight="bold",
        pad=20
    )

    plt.xlabel(
        X_LABEL,
        fontsize=12
    )

    plt.ylabel(
        Y_LABEL,
        fontsize=12
    )

    plt.xticks(
        rotation=ROTATION_ANGLE,
        ha="right",
        fontsize=9
    )

    max_value = max(
        mean_similarities
    )

    plt.ylim(
        0,
        min(
            115,
            max_value + 12
        )
    )

    # Добавляем значения над столбцами (только процент, без имени)
    for bar, value in zip(
            bars,
            mean_similarities
    ):
        height = bar.get_height()
        label = f"{value:.1f}%"  # Только процент

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + VALUE_OFFSET,
            label,
            ha="center",
            va="bottom",
            fontsize=VALUE_FONTSIZE,
            fontweight=VALUE_FONTWEIGHT
            # Убрал rotation=90, теперь текст горизонтальный
        )

    plt.grid(
        axis="y",
        alpha=GRID_ALPHA,
        linestyle=GRID_LINESTYLE
    )

    plt.tight_layout()

    return plt


def save_chart(
        plt_obj
):
    output_path = get_output_path()

    plt_obj.savefig(
        output_path,
        dpi=DPI,
        bbox_inches="tight"
    )

    print(
        f"Chart saved as {output_path}"
    )


def print_table(
        df_sorted
):
    print(
        "\n"
        + "=" * 100
    )

    print(
        f"GRAPHEMATIC NEGATIVE RESULTS FOR {AUTHOR_NAME}"
    )

    print(
        "=" * 100
    )

    print(
        f"{'#':<4} "
        f"{'Compared author':<40} "
        f"{'Mean similarity':<18} "
        f"{'Messages':<12}"
    )

    print(
        "-" * 100
    )

    for i, (_, row) in enumerate(
            df_sorted.iterrows(),
            1
    ):
        print(
            f"{i:<4} "
            f"{row['compared_author']:<40} "
            f"{row['mean_similarity']:<18.2f} "
            f"{row['compared_messages_count']:<12}"
        )


def print_statistics(
        df
):
    print(
        "\n"
        + "=" * 100
    )

    print(
        "STATISTICS"
    )

    print(
        "=" * 100
    )

    min_idx = df[
        "mean_similarity"
    ].idxmin()

    max_idx = df[
        "mean_similarity"
    ].idxmax()

    print(
        f"Profile author: {AUTHOR_NAME}"
    )

    print(
        f"Compared authors: {len(df)}"
    )

    print(
        f"Mean similarity: {df['mean_similarity'].mean():.2f}"
    )

    print(
        f"Median similarity: {df['mean_similarity'].median():.2f}"
    )

    print(
        f"Std similarity: {df['mean_similarity'].std():.2f}"
    )

    print(
        "Min similarity: "
        f"{df.loc[min_idx, 'mean_similarity']:.2f} "
        f"({df.loc[min_idx, 'compared_author']})"
    )

    print(
        "Max similarity: "
        f"{df.loc[max_idx, 'mean_similarity']:.2f} "
        f"({df.loc[max_idx, 'compared_author']})"
    )


def main():
    try:
        file_path = get_file_path()

        print(
            f"Loading data from: {file_path}"
        )

        df = load_data(
            file_path
        )

        print(
            f"Loaded rows: {len(df)}"
        )

        (
            df_sorted,
            authors_full,
            authors_short,
            mean_similarities
        ) = prepare_data(
            df
        )

        plt_obj = create_chart(
            authors_short,
            authors_full,
            mean_similarities
        )

        save_chart(
            plt_obj
        )

        if SHOW_TABLE:
            print_table(
                df_sorted
            )

        if SHOW_STATISTICS:
            print_statistics(
                df
            )

        if SHOW_PLOT:
            plt_obj.show()

    except FileNotFoundError as e:
        print(
            f"Error: {e}"
        )

        print(
            f"Expected path: {get_file_path()}"
        )

    except KeyError as e:
        print(
            f"Error: missing column {e}"
        )

        if "df" in locals():
            print(
                f"Available columns: {df.columns.tolist()}"
            )

    except Exception as e:
        print(
            f"Unexpected error: {e}"
        )


if __name__ == "__main__":
    main()