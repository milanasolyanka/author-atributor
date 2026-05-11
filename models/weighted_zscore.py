# рассчитывает схожесть между двумя векторами признаков с помощью взвешенного z-оценки

import math

# веса признаков для weighted z-score
FEATURE_WEIGHTS = {
    "avg_sentence_length": 1.0,
    "std_sentence_length": 0.8,
    "min_sentence_length": 0.5,
    "max_sentence_length": 0.5,
    "avg_word_length": 1.0,
    "words_per_sentence": 1.0,
    "sentence_length_cv": 0.8,

    "freq_dot": 0.8,
    "freq_comma": 0.8,
    "freq_question": 0.8,
    "freq_exclamation": 0.8,
    "freq_ellipsis": 1.0,
    "freq_dash": 0.8,
    "freq_brackets": 0.5,
    "freq_smiles": 1.2,
    "double_exclamation_rate": 1.0,

    "emoji_rate": 1.0,
    "caps_rate": 0.8,
}

def weighted_z_similarity(
        features,
        means,
        stds,
        weights = FEATURE_WEIGHTS
):
    total_distance = 0
    total_weight = 0

    for feature_name, value in features.items():

        if feature_name not in means:
            continue

        z = abs(
            (value - means[feature_name])
            / stds[feature_name]
        )

        weight = weights.get(
            feature_name,
            1.0
        )

        total_distance += (
            z * weight
        )

        total_weight += weight

    avg_distance = (
        total_distance / total_weight
        if total_weight > 0 else 999
    )

    similarity = math.exp(
        -avg_distance
    )

    percent = similarity * 100

    return round(percent, 2)

