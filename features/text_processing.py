# препроцессинг

import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    return str(text).strip()

def split_sentences(text):
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def tokenize_words(text):
    return re.findall(r"\b\w+\b", text.lower(), flags=re.UNICODE)