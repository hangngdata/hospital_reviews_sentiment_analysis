import gensim.corpora as corpora
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from wordcloud import WordCloud, get_single_color_func

from .text_cleaning import clean_text_wordcloud_lda


def remove_stopwords_and_tokenize_lda(text_series, custom_stopwords_lda):

    stop_words = set(stopwords.words("english")).union(custom_stopwords_lda)

    tokenized = [
        [word for word in word_tokenize(text.lower()) if word.isalpha() and word not in stop_words]
        for text in text_series.dropna()
    ]
    return tokenized

def create_corpus_dictionary(tokenized_texts):
    dictionary = corpora.Dictionary(tokenized_texts)
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_texts]
    return corpus, dictionary

def train_lda(corpus, dictionary, num_topics=4):
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=10,
        alpha='auto',
        per_word_topics=True
    )
    return lda_model

def plot_topic_wordclouds(lda_model, num_topics, hospital_name):
    soft_colors = [
    "#A6CEE3",  # soft blue
    "#B2DF8A",  # soft green
    "#FB9A99",  # soft red/pink
    "#FDBF6F",  # soft orange
    "#CAB2D6",  # soft purple
    "#FFFF99",  # soft yellow
    "#1F78B4",  # darker blue
    "#33A02C",  # darker green
    ]

    fig, axes = plt.subplots(1, num_topics, figsize=(5 * num_topics, 6))

    if num_topics == 1:
        axes = [axes]

    for topic_num in range(num_topics):
        topic_words = dict(lda_model.show_topic(topic_num, topn=20))

        def topic_color_func(*args, **kwargs):
            return soft_colors[topic_num % len(soft_colors)]

        wc = WordCloud(
            width=600,
            height=600,
            background_color='white'
        ).generate_from_frequencies(topic_words)

        wc = wc.recolor(color_func=topic_color_func)

        ax = axes[topic_num]
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"Topic {topic_num + 1}", fontsize=16, fontweight='bold')

    plt.suptitle(hospital_name, fontsize=22, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.show()

def perform_topic_modeling_by_hospital(df, hospital_name, custom_stopwords_lda, num_topics=4):
    df['clean_for_lda'] = df['content'].apply(clean_text_wordcloud_lda)
    hospital_df = df[df["hospital"] == hospital_name]
    text_series = hospital_df["clean_for_lda"]

    tokenized_texts = remove_stopwords_and_tokenize_lda(text_series, custom_stopwords_lda)

    corpus, dictionary = create_corpus_dictionary(tokenized_texts)

    lda_model = train_lda(corpus, dictionary, num_topics=num_topics)

    plot_topic_wordclouds(lda_model, num_topics, hospital_name)

    return lda_model