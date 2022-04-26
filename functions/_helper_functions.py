'''
Autor: Martin Lempp

Kurzbeschreibung:
Hilfsfunktionen für die Analyse'''
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from Levenshtein import distance as levenshtein_distance
from textblob_de import TextBlobDE as TextBlob
from germansentiment import SentimentModel

germansentimentmodel = SentimentModel()

stemmer = SnowballStemmer("german")
stop_words = set(stopwords.words("german"))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clean_text(txt):
    """
        - remove any html tags (< /br> often found)
        - Keep only ASCII + European Chars and whitespace, no digits
        - remove single letter chars
        - convert all whitespaces (tabs etc.) to single wspace
        if not for embedding (but e.g. tdf-idf):
        - all lowercase
        - remove stopwords, punctuation and stemm
    """
    RE_WSPACE = re.compile(r"\s+", re.IGNORECASE)
    RE_TAGS = re.compile(r"<[^>]+>")
    RE_ASCII = re.compile(r"[^A-Za-zÀ-ž ]", re.IGNORECASE)
    RE_SINGLECHAR = re.compile(r"\b[A-Za-zÀ-ž]\b", re.IGNORECASE)

    txt = re.sub(RE_TAGS, " ", txt)
    txt = re.sub(RE_ASCII, " ", txt)
    txt = re.sub(RE_SINGLECHAR, " ", txt)
    txt = re.sub(RE_WSPACE, " ", txt)

    word_tokens = word_tokenize(txt)
    words_tokens_lower = [word.lower() for word in word_tokens]

    words_filtered = [
        stemmer.stem(word) for word in words_tokens_lower if word not in stop_words
    ]

    text_clean = " ".join(words_filtered)
    return text_clean


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_sentiment_score_from_dict_per_word(word,dct):
    return dct[list(dct.keys())[np.argmin([levenshtein_distance(x, word) for x in dct.keys()])]]


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_sentiment_score_from_dict_mean(txt,dct):
    if not pd.isna(txt):
        words = txt.split()
        score = [calc_sentiment_score_from_dict_per_word(word,dct) for word in words]
        return np.mean(score)
    else:
        return np.nan


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_sentiment_score1_sum_txt(txt,dct):
    if not pd.isna(txt):
        words = txt.split()
        score = [calc_sentiment_score_from_dict_per_word(word,dct) for word in words]
        return np.sum(score)
    else:
        return np.nan


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_sentiment_score2(txt):
    if not pd.isna(txt):
        return germansentimentmodel.predict_sentiment([txt])
    else:
        return np.nan


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_sentiment_score3(txt):
    if not pd.isna(txt):
        return TextBlob(txt).sentiment.polarity
    else:
        return np.nan


