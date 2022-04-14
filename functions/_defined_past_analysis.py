'''
Autor: Martin Lempp

Kurzbeschreibung:
Analysiere videos eines vergangenen Zeitraums bis heute
'''
import pandas as pd
import os
import sys
from tqdm import tqdm
from collections import Counter
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _video_class import *
import json
from datetime import date
from germansentiment import SentimentModel


def defined_past_analysis(path, delta = 14, calc_sentiment_score1 = False, calc_sentiment_score2 = False, calc_sentiment_score3 = False):
    today = date.today()
    limit = pd.to_datetime(today)-pd.to_timedelta(delta, unit = 'd')

    # load full video df
    # load full comment df


    outpath = path + 'out/'
    video_df = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)

    with open(path + 'comment_DataBase.json', 'r') as jsonfile:
        comment_dict = json.load(jsonfile)



    video_df.video_date = pd.to_datetime(video_df.video_date)
    video_df_red = video_df[video_df.video_date > limit]
    video_ids_OI = list(video_df_red.index)


    video_dct = {}
    for id in tqdm(video_ids_OI):
        tmp_video = video_df.loc[id]
        tmp_comment = comment_df.loc[id]
        tmp_class = video(id, tmp_video.video_title, tmp_video.video_date, path)
        tmp_class.add_comments(tmp_comment.comments)
        tmp_class.prep_comments()
        video_dct[id] = tmp_class
        if calc_sentiment_score1:
            model = SentimentModel()
            tmp_class.calc_sentiment_score2(model)

        if calc_sentiment_score2:
            model = SentimentModel()
            tmp_class.calc_sentiment_score2(model)

        if calc_sentiment_score3:
            tmp_class.calc_sentiment_score3()


