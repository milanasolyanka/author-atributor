# загружает csv

import pandas as pd
from config import TEXT_COLUMN


def load_author_csv(csv_path):
    df = pd.read_csv(csv_path)

    df = df.dropna(subset=[TEXT_COLUMN])

    df[TEXT_COLUMN] = (
        df[TEXT_COLUMN]
        .astype(str)
        .str.strip()
    )

    df = df[df[TEXT_COLUMN] != ""]

    return df