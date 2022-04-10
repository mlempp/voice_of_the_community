import pandas as pd
import os
from tqdm import tqdm
from collections import Counter
path = os.getcwd() + '/'
from _video_class import *
from datetime import date


def defined_past_analysis(delta,outpath):
    today = date.today()
    limit = pd.to_datetime(today)-pd.to_timedelta(delta, unit = 'd')

    outpath = path + 'out/'
    video_df = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
    video_df.video_date = pd.to_datetime(video_df.video_date)
    video_df_red = video_df[video_df.video_date > limit]
    video_ids_OI = list(video_df_red.index)



    pass