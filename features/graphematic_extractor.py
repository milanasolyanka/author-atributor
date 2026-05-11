import re


def extract_graphematic_features(
        text
):
    return {
        "dot_rate_100": extract_dot_rate_100(
            text
        ),
        "comma_rate_100": extract_comma_rate_100(
            text
        ),
        "dash_rate_100": extract_dash_rate_100(
            text
        ),
        "exclamation_rate_100": extract_exclamation_rate_100(
            text
        ),
        "question_rate_100": extract_question_rate_100(
            text
        ),
        "yo_percent": extract_yo_percent(
            text
        ),
        "uppercase_percent": extract_uppercase_percent(
            text
        ),
        "quote_type": extract_quote_type(
            text
        ),
        "dash_type": extract_dash_type(
            text
        ),
    }


# ==========================================================
# HELPERS
# ==========================================================

def _safe_divide(
        value,
        total
):
    """
    Безопасное деление.
    """

    if total == 0:
        return 0

    return value / total


# ==========================================================
# PUNCTUATION
# ==========================================================

def extract_dot_rate_100(
        text
):
    """
    Количество точек
    на 100 символов.
    """

    total_chars = max(
        len(text),
        1
    )

    return (
        text.count(".")
        / total_chars
    ) * 100


def extract_comma_rate_100(
        text
):
    """
    Количество запятых
    на 100 символов.
    """

    total_chars = max(
        len(text),
        1
    )

    return (
        text.count(",")
        / total_chars
    ) * 100


def extract_dash_rate_100(
        text
):
    """
    Количество тире
    на 100 символов.

    Считает:
    -
    —
    –
    """

    total_chars = max(
        len(text),
        1
    )

    dash_count = (
        text.count("-")
        + text.count("—")
        + text.count("–")
    )

    return (
        dash_count
        / total_chars
    ) * 100


def extract_exclamation_rate_100(
        text
):
    """
    Количество !
    на 100 символов.
    """

    total_chars = max(
        len(text),
        1
    )

    return (
        text.count("!")
        / total_chars
    ) * 100


def extract_question_rate_100(
        text
):
    """
    Количество ?
    на 100 символов.
    """

    total_chars = max(
        len(text),
        1
    )

    return (
        text.count("?")
        / total_chars
    ) * 100


# ==========================================================
# GRAPHEMATIC ANALYSIS
# ==========================================================

def extract_yo_percent(
        text
):
    """
    Процент букв Ё/ё
    от количества символов.
    """

    total_chars = max(
        len(text),
        1
    )

    yo_count = (
        text.count("Ё")
        + text.count("ё")
    )

    return (
        yo_count
        / total_chars
    ) * 100


def extract_uppercase_percent(
        text
):
    """
    Процент заглавных букв
    от количества символов.
    """

    total_chars = max(
        len(text),
        1
    )

    uppercase_count = sum(
        1
        for char in text
        if char.isalpha()
        and char.isupper()
    )

    return (
        uppercase_count
        / total_chars
    ) * 100


def extract_quote_type(
        text
):
    """
    Тип кавычек.

    Возвращает:
    - «елочки»
    - "лапки"
    - "нет"
    """

    has_angled = (
        "«" in text
        or "»" in text
    )

    has_double = (
        '"' in text
    )

    if has_angled:
        return "елочки"

    if has_double:
        return "лапки"

    return "нет"


def extract_dash_type(
        text
):
    """
    Вид тире.

    Возвращает:
    - дефис
    - двойное
    - тройное
    - нет
    """

    triple_dash = (
        "---" in text
        or "———" in text
    )

    double_dash = (
        "--" in text
        or "——" in text
    )

    single_dash = (
        "-" in text
        or "—" in text
        or "–" in text
    )

    if triple_dash:
        return "тройное"

    if double_dash:
        return "двойное"

    if single_dash:
        return "дефис"

    return "нет"
