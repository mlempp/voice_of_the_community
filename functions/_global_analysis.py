import pandas as pd
import os
from tqdm import tqdm
from collections import Counter
path = os.getcwd() + '/'
from _video_class import *
from datetime import datetime as timer
from datetime import date
import json
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")


def _global_analysis(path, save_word_count = True):

    outpath = path + 'out/'
    video_df = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
    video_ids_OI = list(video_df.index)

    comment_df = pd.read_csv(path+'comment_DataBase.csv', sep = ';', index_col = 0)

    video_dct = {}
    full_comment_list =[]
    full_preped_comment_list =[]
    for id in tqdm(video_ids_OI):
        tmp_video = video_df.loc[id]
        tmp_comment = comment_df.loc[id]
        tmp_class = video(id, tmp_video.video_title, tmp_video.video_date)
        tmp_class.add_comments(tmp_comment.comments)
        tmp_class.prep_comments()
        full_comment_list = full_comment_list+tmp_class.comments_list
        full_preped_comment_list = full_preped_comment_list+tmp_class.comments_list_preped
        video_dct[id] = tmp_class

    if save_word_count:
        all_words_list = [x.split() for x in full_preped_comment_list]
        all_words_flat = [ item for elem in all_words_list for item in elem]
        count_dict = Counter(all_words_flat)

        with open(d+'_global_word_count.json', 'w') as fp:
            json.dump(dict(count_dict), fp)




    #most frequent words
    #sentiment per week

    pass