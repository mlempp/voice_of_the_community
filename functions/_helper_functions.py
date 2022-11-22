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
import os
import pickle
import platform
from Levenshtein import distance as levenshtein_distance
from textblob_de import TextBlobDE as TextBlob
from germansentiment import SentimentModel
from random import choice

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
    dict_words = np.array(list(dct.keys()))
    dict_values = np.array(list(dct.values()))
    dist = np.array([levenshtein_distance(x, word) for x in dict_words])
    if dist.min() < 2:
        close = np.argwhere(dist<2).reshape(-1)
        all_sentis = dict_values[close]
        senti = all_sentis.mean()
    else:
        senti = 0
    return senti


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_sentiment_scores_from_dict(txt,dct):
    if not pd.isna(txt):
        words = txt.split()
        senti_list = np.array([calc_sentiment_score_from_dict_per_word(word,dct) for word in words])
        s_mean = np.mean(senti_list)
        s_median = np.median(senti_list)
        s_sum = np.sum(senti_list)
        s_ratio = (sum(senti_list > 0) - sum(senti_list < 0)) / (senti_list.size+1)
        return s_mean, s_sum,s_median, s_ratio
    else:
        return np.nan, np.nan, np.nan, np.nan

#
# #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def calc_sentiment_score_from_dict_ratio(txt,dct):
#     if not pd.isna(txt):
#         words = txt.split()
#         senti_list = np.array([calc_sentiment_score_from_dict_per_word(word,dct) for word in words])
#         return (sum(senti_list > 0) - sum(senti_list < 0)) / (senti_list.size+1)
#     else:
#         return np.nan
#
#
# #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def calc_sentiment_score_from_dict_mean(txt,dct):
#     if not pd.isna(txt):
#         words = txt.split()
#         senti_list = [calc_sentiment_score_from_dict_per_word(word,dct) for word in words]
#         return np.mean(senti_list)
#     else:
#         return np.nan
#
#
# #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def calc_sentiment_score_from_dict_sum(txt,dct):
#     if not pd.isna(txt):
#         words = txt.split()
#         senti_list = [calc_sentiment_score_from_dict_per_word(word,dct) for word in words]
#         return np.sum(senti_list)
#     else:
#         return np.nan
#
#
# #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def calc_sentiment_score_from_dict_median(txt,dct):
#     if not pd.isna(txt):
#         words = txt.split()
#         senti_list = [calc_sentiment_score_from_dict_per_word(word,dct) for word in words]
#         return np.median(senti_list)
#     else:
#         return np.nan
#

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


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def load_newest_comment_file(path):
    comment_files = [x for x in os.listdir(path) if 'comment_DataBase' in x]
    comment_files.sort()
    comment_file = comment_files[-1]
    if  (platform.system() == 'Windows'):
        df = pd.read_csv(path + comment_file, sep=';', index_col=0)
    else:
        # df = pd.read_csv(path + comment_file, sep=';', index_col=0, lineterminator='\r')
        df = pd.read_csv(path + comment_file, sep=';', index_col=0)

    return df

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def load_best_clf_model(path):
    model_files = [x for x in os.listdir(path) if 'best_model' in x]
    model_files.sort()
    model_file = model_files[-1]
    return pickle.load(open(path + model_file, 'rb')), model_file

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def load_newest_clf_models(path):
    model_dates = [int(x[:13].replace('_', '')) for x in os.listdir(path) if 'sav' in x]
    model_dates_unique = list(set(model_dates))
    model_dates_unique.sort()
    newest_date = str(model_dates_unique[-1])
    newest_date = newest_date[:6] + '_' + newest_date[6:]

    model_files = [x for x in os.listdir(path) if ('clf' in x) & (newest_date in x) & ('best_model' not in x)]
    models = []
    for m in model_files:
        models.append(pickle.load(open(path + m, 'rb')))
    return models

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def translate_pos(value):
    if value > 0:
        return 1
    else:
        return 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def translate_neg(value):
    if value < 0:
        return 1
    else:
        return 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def translate_neu(value):
    if value == 0:
        return 1
    else:
        return 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def translate_to_class(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_word_counts(words_oi, string):
    count_dct = {}
    for woi in words_oi:
        count = string.count(woi.lower())
        if count > 0:
            count_dct[woi] = np.sum(count)

    return count_dct

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_most_freq(dct):
    dct_values = list(dct.values())
    dct_names = list(dct.keys())

    max_count = np.max(dct_values)
    max_count_index = [i for i,x in enumerate(dct_values) if x == max_count ]
    return dct_names[choice(max_count_index)]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_least_freq(dct):
    dct_values = list(dct.values())
    dct_names = list(dct.keys())

    min_count = np.min(dct_values)
    min_count_index = [i for i,x in enumerate(dct_values) if x == min_count ]
    return dct_names[choice(min_count_index)]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_carmodel_counts(models, cs_lst):
    cs_lst_lower = [x.lower() for x in cs_lst]
    count_dct = {}
    for i, model_row in models.iterrows():
        kennung = model_row.Kennung.split('|')
        kennung = [x.lower() for x in kennung]
        model = model_row.Model
        kennung_cs = [comment for comment in cs_lst_lower if any(x in comment for x in kennung)]
        if len(kennung_cs):
            count_dct[model] = len(kennung_cs)
    return count_dct

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_breaks_before_space(string):
    updated_string = ''
    cnt = 0
    for letter in string:
        cnt += 1
        if (letter == ' ' ) & (cnt > 120):
            updated_string = updated_string+'<br>'
            cnt = 0
        else:
            updated_string = updated_string + letter

    return updated_string

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def cut_sentence(string):
    updated_string = ''
    cnt = 0
    for letter in string:
        cnt += 1
        if (letter == ' ' ) & (cnt > 60):
            updated_string = updated_string+'...'
            break
        else:
            updated_string = updated_string + letter
    return updated_string

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def input_yes_no(string):
    answer = input(string).upper()
    while answer not in ['YES', 'NO']:
        answer = input(string).upper()
    return answer

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def input_date(string):
    answer = input(string)
    date = None
    while date is None:
        try:
            date = pd.to_datetime(answer, format='%d.%m.%Y')
        except:
            pass
    return date



