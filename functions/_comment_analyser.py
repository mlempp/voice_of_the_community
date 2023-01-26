'''
Autor: Martin Lempp

Kurzbeschreibung:
Analyse einer Kommentarserie
'''
import os
import pickle
import pandas as pd
from functions._helper_functions import *
import numpy as np
from scipy import stats
from collections import Counter


def analyse_comments(csoi, path):
    csoi = csoi.copy()
    #load newst model
    model,_ = load_best_clf_model(path+'analyse/')
    models = load_newest_clf_models(path+'analyse/')

    #load all lists
    parts = pd.read_csv(path+'functions/'+'bauteile.csv', encoding = 'utf-8', header = None)[0].to_list()
    colors = pd.read_csv(path+'functions/'+'farbliste.csv', encoding = 'utf-8', header = None)[0].to_list()
    brands = pd.read_csv(path+'functions/'+'markenliste.csv', encoding = 'utf-8', header = None)[0].to_list()
    carmodels = pd.read_csv(path+'functions/'+'modelliste_2.csv', encoding = 'iso8859_2', sep =';')
    columns_OI = ['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3', 'Sentiment_score_4', 'Sentiment_score_5', 'Sentiment_score_6',
                  'Sentiment_score_10', 'Sentiment_score_11', 'Sentiment_score_7', 'Sentiment_score_8', 'Sentiment_score_9', 'Sentiment_score_12',
                  'Sentiment_score_13', 'Sentiment_score_14']
    #annotate comments
    csoi_red = csoi[ (~ csoi.Sentiment_score_1.isin([np.nan, np.inf, ''])) &
                     (~ csoi.Sentiment_score_3.isin([np.nan, np.inf, ''])) &
                     (~ csoi.Sentiment_score_4.isin([np.nan, np.inf, ''])) &
                     (~ csoi.Sentiment_score_5.isin([np.nan, np.inf, ''])) &
                     (csoi.Sentiment_score_2.isin(["['negative']", "['neutral']", "['positive']"]))].copy()
    csoi_red['Sentiment_score_2_update'] = csoi_red.Sentiment_score_2.replace({"['negative']": -1, "['neutral']": 0, "['positive']": 1})
    predictors = csoi_red[columns_OI].copy()
    csoi_red['annotations_best'] = model.predict(predictors)

    for i,m in enumerate(models):
        if i == 0:
            pred_ensemle = np.array([m.predict(predictors)])
        else:
            pred_ensemle = np.append(pred_ensemle, [m.predict(predictors)], axis = 0)
    csoi_red['annotations_ensemble'] = stats.mode(pred_ensemle).mode[0]

    #prep comments and make word count
    comment_string = ' '.join(csoi_red.comment.to_list()).lower()
    preped_comment_string = ' '.join(csoi_red.comment_preped.to_list()).lower()

    # unique_word_count = Counter(comment_string.split())
    # unique_preped_words_count = Counter(preped_comment_string.split())

    #count annotations
    pos_coms = csoi_red[csoi_red['annotations_ensemble'] == 1].copy()
    num_pos_coms = pos_coms.shape[0]
    part_pos_coms = num_pos_coms / csoi_red.shape[0]

    neu_coms = csoi_red[csoi_red['annotations_ensemble'] == 0].copy()
    num_neu_coms = neu_coms.shape[0]
    part_neu_coms = num_neu_coms / csoi_red.shape[0]

    neg_coms = csoi_red[csoi_red['annotations_ensemble'] == -1].copy()
    num_neg_coms = neg_coms.shape[0]
    part_neg_coms = num_neg_coms / csoi_red.shape[0]

    rand_pos_comment = pos_coms[pos_coms.comment.apply(lambda x: len(x)) < 250].sample(n=1).comment.iloc[0]

    #count color
    color_counts = get_word_counts(colors, comment_string)
    most_freq_color = get_most_freq(color_counts).strip()
    least_freq_color = get_least_freq(color_counts).strip()


    #count marke
    brand_counts = get_word_counts(' | '.join(brands).split('|'), comment_string)
    most_freq_brand = get_most_freq(brand_counts).strip()
    least_freq_brand = get_least_freq(brand_counts).strip()

    #count model
    carmodels_count = get_carmodel_counts(carmodels, csoi_red.comment.to_list())
    most_freq_model = get_most_freq(carmodels_count).strip()
    least_freq_model = get_least_freq(carmodels_count).strip()

    #count part
    part_counts = get_word_counts(parts, comment_string)
    most_freq_part = get_most_freq(part_counts).strip()
    least_freq_part = get_least_freq(part_counts).strip()

    return {'part_pos_coms':part_pos_coms,
            'part_neu_coms':part_neu_coms,
            'part_neg_coms':part_neg_coms,
            'most_freq_color':most_freq_color,
            'least_freq_color':least_freq_color,
            'most_freq_brand':most_freq_brand,
            'least_freq_brand':least_freq_brand,
            'most_freq_model':most_freq_model,
            'least_freq_model':least_freq_model,
            'most_freq_part':most_freq_part,
            'least_freq_part':least_freq_part,
            'rand_pos_comment': rand_pos_comment}