#  эвристическая rule-based similarity metric.

import pandas as pd


# ==========================================================
# CONFIG
# ==========================================================

NUMERIC_FEATURES = [
    "dot_rate_100",
    "comma_rate_100",
    "dash_rate_100",
    "exclamation_rate_100",
    "question_rate_100",
    "yo_percent",
    "uppercase_percent",
]

CATEGORICAL_FEATURES = [
    "quote_type",
    "dash_type",
]


# ==========================================================
# PROFILE
# ==========================================================

def build_heuristic_profile(
        train_df,
        extract_features
):
    """
    Строит профиль автора.

    Числовые признаки:
    -> среднее значение.

    Категориальные:
    -> мода (самое частое).
    """

    feature_rows = []

    for text in train_df["text"]:
        features = extract_features(
            text
        )

        if features:
            feature_rows.append(
                features
            )

    feature_df = pd.DataFrame(
        feature_rows
    )

    profile = {}

    # =====================
    # Numeric
    # =====================

    for feature in (
            NUMERIC_FEATURES
    ):
        profile[feature] = (
            feature_df[
                feature
            ].mean()
        )

    # =====================
    # Categorical
    # =====================

    for feature in (
            CATEGORICAL_FEATURES
    ):
        mode_series = (
            feature_df[
                feature
            ].mode()
        )

        profile[feature] = (
            mode_series.iloc[0]
            if not mode_series.empty
            else "нет"
        )

    return profile


# ==========================================================
# FEATURE SCORING
# ==========================================================

def score_numeric_feature(
        difference
):
    """
    Rule-based score.

    Чем меньше разница,
    тем больше балл.
    """

    if difference <= 0.5:
        return 100

    if difference <= 2:
        return 75

    if difference <= 5:
        return 50

    if difference <= 10:
        return 25

    return 0


def score_categorical_feature(
        text_value,
        profile_value
):
    """
    Совпали → 100
    Не совпали → 0
    """

    return (
        100
        if text_value
           == profile_value
        else 0
    )


# ==========================================================
# SIMILARITY
# ==========================================================

def heuristic_similarity(
        features,
        profile
):
    """
    Эвристическая
    similarity metric.
    """

    total_score = 0
    max_score = 0

    # =====================
    # Numeric features
    # =====================

    for feature in (
            NUMERIC_FEATURES
    ):
        if (
                feature
                not in features
                or feature
                not in profile
        ):
            continue

        difference = abs(
            features[feature]
            - profile[feature]
        )

        score = (
            score_numeric_feature(
                difference
            )
        )

        total_score += score
        max_score += 100

    # =====================
    # Categorical
    # =====================

    for feature in (
            CATEGORICAL_FEATURES
    ):
        if (
                feature
                not in features
                or feature
                not in profile
        ):
            continue

        score = (
            score_categorical_feature(
                features[
                    feature
                ],
                profile[
                    feature
                ]
            )
        )

        total_score += score
        max_score += 100

    # =====================
    # Final similarity
    # =====================

    if max_score == 0:
        return 0

    similarity = (
        total_score
        / max_score
    ) * 100

    return round(
        similarity,
        2
    )