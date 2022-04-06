import pandas as pd
import os
from tqdm import tqdm
from collections import Counter
path = os.getcwd() + '/'
from _video_class import *


def _global_analysis(path):

    outpath = path + 'out/'
    video_df = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
    video_ids_OI = list(video_df.index)

    comment_df = pd.read_csv(path+'comment_DataBase.csv', sep = ';', index_col = 0)

    video_dct = {}
    full_comment_list =[]
    for id in tqdm(video_ids_OI):
        tmp_video = video_df.loc[id]
        tmp_comment = comment_df.loc[id]
        tmp_class = video(id, tmp_video.video_title, tmp_video.video_date)
        tmp_class.add_comments(tmp_comment.comments)
        tmp_class.prep_comments()
        full_comment_list = full_comment_list+tmp_class.comments_list
        video_dct[id] = tmp_class


    all_words_list = [x.split() for x in full_comment_list]
    all_words_flat = [ item for elem in all_words_list for item in elem]
    count_dict = dict((x, all_words_flat.count(x)) for x in set(all_words_flat))




    #most frequent words
    #sentiment per week

    pass