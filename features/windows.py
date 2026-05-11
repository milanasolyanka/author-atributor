from features.text_processing import clean_text


def create_windows(text, window_size=500, step=250):
    text = clean_text(text)

    windows = []

    if len(text) <= window_size:
        windows.append(text)
        return windows

    for start in range(
        0,
        len(text) - window_size + 1,
        step
    ):
        end = start + window_size
        windows.append(text[start:end])

    return windows