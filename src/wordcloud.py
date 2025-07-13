import re
import string
import unicodedata

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords

from wordcloud import WordCloud, get_single_color_func

from .text_cleaning import clean_text_wordcloud_lda


def remove_stopwords_and_short_wordcloud(text, custom_stopwords_wordcloud):
    stop_words = set(stopwords.words("english")).union(custom_stopwords_wordcloud)
    words = text.split()
    words = [word for word in words 
             if word not in stop_words and len(word) > 2]
    return " ".join(words)

def plot_wordcloud_by_hospital(df, hospital_name, custom_stopwords_wordcloud, background_color="white", max_words=100):
    df['clean_for_wordcloud'] = df['content'].apply(clean_text_wordcloud_lda)
    df['clean_for_wordcloud'] = df['clean_for_wordcloud'].apply(
        lambda x: remove_stopwords_and_short_wordcloud(x, custom_stopwords_wordcloud)
        )
    hospital_df = df.loc[df["hospital"] == hospital_name].copy()
    all_text = " ".join(hospital_df['clean_for_wordcloud'])

    hospital_color = {
        "UZ Leuven Gasthuisberg": "#00B5E2",
        "UZ Leuven Pellenberg": "#00B5E2",
        "UZ Gent": "#0066CC",
        "UZ Antwerpen": "#E22335",
        "UZ Brussel": "#9BA23F"
    }

    color_hex = hospital_color.get(hospital_name, "#000000")
    color_func = get_single_color_func(color_hex)

    wordcloud = WordCloud(
        random_state=512,
        width=1200,
        height=600,
        background_color=background_color,
        max_words=max_words,
        contour_color='steelblue',
        contour_width=1
    ).generate(all_text)

    wordcloud.recolor(color_func=color_func)

    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(
        f"Most Frequent Words in Patient Reviews\n{hospital_name}",
        fontsize=24,
        fontweight='bold',
        color='black',
        pad=30,
        backgroundcolor='whitesmoke'
    )
    plt.tight_layout(pad=2)
    plt.show()