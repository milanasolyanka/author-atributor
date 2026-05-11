# извлекает признаки из текста

import re
import numpy as np

from features.text_processing import clean_text, split_sentences, tokenize_words


FUNCTION_WORDS = [
    "ну", "вот", "же", "то", "ли", "как", "бы",
    "прям", "типа", "короче", "просто",
    "вообще", "блин", "даже", "только"
]

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002700-\U000027BF"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)

def extract_features(text):
    text = clean_text(text)

    if len(text.strip()) == 0:
        return {}

    sentences = split_sentences(text)
    words = tokenize_words(text)

    sentence_lengths = [len(tokenize_words(s)) for s in sentences]

    if len(sentence_lengths) == 0:
        sentence_lengths = [0]

    total_chars = max(len(text), 1)
    total_words = max(len(words), 1)
    total_sentences = max(len(sentences), 1)

    features = {}

    # ======================
    # Rhythm
    # ======================

    features["avg_sentence_length"] = np.mean(sentence_lengths)
    features["std_sentence_length"] = np.std(sentence_lengths)
    features["min_sentence_length"] = np.min(sentence_lengths)
    features["max_sentence_length"] = np.max(sentence_lengths)

    word_lengths = [len(w) for w in words]
    features["avg_word_length"] = (
        np.mean(word_lengths) if word_lengths else 0
    )

    features["words_per_sentence"] = (
        total_words / total_sentences
    )

    mean_len = np.mean(sentence_lengths)

    features["sentence_length_cv"] = (
        np.std(sentence_lengths) / mean_len
        if mean_len > 0 else 0
    )

    # ======================
    # Punctuation
    # ======================

    features["freq_dot"] = text.count(".") / total_chars
    features["freq_comma"] = text.count(",") / total_chars
    features["freq_question"] = text.count("?") / total_chars
    features["freq_exclamation"] = text.count("!") / total_chars

    ellipsis_count = (
        text.count("...")
        + text.count("…")
    )

    features["freq_ellipsis"] = (
        ellipsis_count / total_chars
    )

    dash_count = (
        text.count("-")
        + text.count("—")
    )

    features["freq_dash"] = dash_count / total_chars

    brackets_count = (
        text.count("(")
        + text.count(")")
    )

    features["freq_brackets"] = (
        brackets_count / total_chars
    )

    smile_matches = re.findall(r"\){2,}", text)
    features["freq_smiles"] = (
        len(smile_matches) / total_chars
    )

    double_exclam = len(
        re.findall(r"!!+", text)
    )

    features["double_exclamation_rate"] = (
        double_exclam / total_chars
    )

    # ======================
    # Function words
    # ======================

    word_counter = {}

    for w in words:
        word_counter[w] = (
            word_counter.get(w, 0) + 1
        )

    for word in FUNCTION_WORDS:
        features[f"fw_{word}"] = (
            word_counter.get(word, 0)
            / total_words
        )

    # ======================
    # Additional
    # ======================

    emoji_count = len(
        EMOJI_PATTERN.findall(text)
    )

    features["emoji_rate"] = (
        emoji_count / total_chars
    )

    caps_words = sum(
        1 for w in re.findall(r"\b\w+\b", text)
        if len(w) > 1 and w.isupper()
    )

    features["caps_rate"] = (
        caps_words / total_words
    )

    return features

