import warnings

import pandas as pd
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

warnings.filterwarnings('ignore')

analyzer = SentimentIntensityAnalyzer()
def analyze_vader_sentiment(text):
    if pd.isnull(text) or text.strip() == "":
        return pd.Series({"vader_positive": 0, "vader_neutral": 0, "vader_negative": 0, "vader_compound": 0, "vader_sentiment": "neutral"})
    
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    pos = scores["pos"]
    neg = scores["neg"]
    neu = scores["neu"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.5:
        label = "negative"
    else:
        label = "neutral"

    return pd.Series({
        "vader_positive": pos,
        "vader_neutral": neu,
        "vader_negative": neg,
        "vader_compound": compound,
        "vader_sentiment": label
    })


sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
def analyze_distilbert_sentiment(df, text_column="content", label_column="distilbert_label", score_column="distilbert_score"):
    def analyze(text):
        if not text or text.strip() == "":
            return pd.Series({label_column: None, score_column: None})
        result = sentiment_pipeline(text[:512])[0]
        return pd.Series({label_column: result["label"].lower(), score_column: result["score"]})

    df[[label_column, score_column]] = df[text_column].apply(analyze)
    return df
