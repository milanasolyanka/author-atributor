# делит на тренирововчную и тестовую выборки

from sklearn.model_selection import train_test_split


def split_dataset(
    df,
    train_size,
    random_seed
):
    return train_test_split(
        df,
        train_size=train_size,
        random_state=random_seed,
        shuffle=True
    )