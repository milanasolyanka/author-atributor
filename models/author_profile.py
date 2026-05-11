#  построение профиля автора

import pandas as pd

from config import TEXT_COLUMN
from features.feature_extractor import extract_features


def build_author_profile(train_df):
    feature_rows = []

    for text in train_df[TEXT_COLUMN]:
        features = extract_features(text)

        if features:
            feature_rows.append(features)

    feature_df = pd.DataFrame(feature_rows)

    means = feature_df.mean()
    stds = feature_df.std()

    stds = stds.replace(0, 1e-6)

    return means, stds