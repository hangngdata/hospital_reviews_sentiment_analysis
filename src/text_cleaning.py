import re
import string
import unicodedata

import pandas as pd


def clean_text_wordcloud_lda(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r"http\S+", "", text)
    text = text.replace("#", "")
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def reduce_elongation(text):
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def clean_text_sentiment(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = text.strip()
    text = text.lower()
    text = reduce_elongation(text)
    text = text.strip()
    return text