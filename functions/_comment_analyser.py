'''
Autor: Martin Lempp

Kurzbeschreibung:
Analyse einer Kommentarserie
'''
import os
import pickle
import pandas as pd
from _helper_functions import *
import numpy as np


def analyse_comments(csoi, path):
    csoi = csoi.copy()
    #load newst model
    model = load_newest_model(path+'analyse/')

    #load all lists
    parts = pd.read_csv(path+'functions/'+'bauteile.csv')
    colors = pd.read_csv(path+'functions/'+'farbliste.csv', encoding = 'iso8859_2')
    brands = pd.read_csv(path+'functions/'+'markenliste.csv', encoding = 'iso8859_2')
    models = pd.read_csv(path+'functions/'+'modelliste.csv', encoding = 'iso8859_2')

    #annotate comments
    csoi_red = csoi[ (~ csoi.Sentiment_score_1.isin([np.nan, np.inf, ''])) &
                     (~ csoi.Sentiment_score_3.isin([np.nan, np.inf, ''])) &
                     (~ csoi.Sentiment_score_4.isin([np.nan, np.inf, ''])) &
                     (~ csoi.Sentiment_score_5.isin([np.nan, np.inf, ''])) &
                     (csoi.Sentiment_score_2.isin(["['negative']", "['neutral']", "['positive']"]))].copy()
    csoi_red['Sentiment_score_2_update'] = csoi_red.Sentiment_score_2.replace({"['negative']": -1, "['neutral']": 0, "['positive']": 1})
    predictors = csoi_red[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]].copy()
    csoi_red['annotations'] = model.predict(predictors)

    #prep comments and make word count


    #count annotations
    pos_coms = csoi_red[csoi_red['annotations'] == 1].copy()
    num_pos_coms = pos_coms.shape[0]
    part_pos_coms = num_pos_coms / csoi_red.shape[0]

    neu_coms = csoi_red[csoi_red['annotations'] == 0].copy()
    num_neu_coms = neu_coms.shape[0]
    part_neu_coms = num_neu_coms / csoi_red.shape[0]

    neg_coms = csoi_red[csoi_red['annotations'] == -1].copy()
    num_neg_coms = neg_coms.shape[0]
    part_neg_coms = num_neg_coms / csoi_red.shape[0]

    rand_pos_comment = pos_coms.sample(n=1).comment.iloc[0]

    #count color
    most_freq_color
    least_freq_color


    #count marke
    most_freq_brand
    least_freq_brand

    #count model
    most_freq_model
    least_freq_model

    #count part
    most_freq_part
    least_freq_part

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