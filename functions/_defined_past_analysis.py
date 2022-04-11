import pandas as pd
import os
import sys
from tqdm import tqdm
from collections import Counter
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _video_class import *
from datetime import date
from germansentiment import SentimentModel


def defined_past_analysis(delta, path, calc_sentiment_score2 = False):
    today = date.today()
    limit = pd.to_datetime(today)-pd.to_timedelta(delta, unit = 'd')

    outpath = path + 'out/'
    video_df = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
    video_df.video_date = pd.to_datetime(video_df.video_date)
    video_df_red = video_df[video_df.video_date > limit]
    video_ids_OI = list(video_df_red.index)

    comment_df = pd.read_csv(path+'comment_DataBase.csv', sep = ';', index_col = 0)

    video_dct = {}
    for id in tqdm(video_ids_OI):
        tmp_video = video_df.loc[id]
        tmp_comment = comment_df.loc[id]
        tmp_class = video(id, tmp_video.video_title, tmp_video.video_date, path)
        tmp_class.add_comments(tmp_comment.comments)
        tmp_class.prep_comments()
        video_dct[id] = tmp_class
        if calc_sentiment_score2:
            model = SentimentModel()
            tmp_class.calc_sentiment_score2(model)


