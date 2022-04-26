'''
Autor: Martin Lempp

Kurzbeschreibung:
Hauptprogramm zur Sentimentanalyse und Report-Erstellung
'''
import pandas as pd
import os
from datetime import datetime as timer
from datetime import date
import sys
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _generate_update_comment_database import *
from _generate_update_video_database import *
from _video_class import *
from _defined_past_analysis import *
from _update_thumbnail_database import *
from _global_analysis import *
from _yearly_analysis import *




def main():
    path = os.getcwd() + '/'

    video_database_update(path)
    comment_database_update(path)
    thumbnail_database_update(path)

    # global_analysis(path = path)
    # defined_past_analysis(start =  '01.01.2021', stop = '31.12.2021' , path = path)
    # defined_past_analysis(delta='14d', path = path,calc_sentiment_score2 = True)

    pass



for i, row in tqdm(df_comments.iterrows(), total = df_comments.shape[0]):
    txt = row.comment_preped
    df_comments.loc[i, 'Sentiment_score_4'] = calc_sentiment_score_from_dict_mean(txt, senti_4_polarity)
