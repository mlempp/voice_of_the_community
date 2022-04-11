import os
import sys
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _helper_functions import *
import pandas as pd

class video:
    def __init__(self, video_id, video_title, video_date):
        self.video_id = video_id
        self.video_title = video_title
        self.video_date = video_date
        senti_ws_positive = pd.read_csv(path + 'functions/SentiWS_v1.8c_Positive.txt', sep = '\t', header = None)
        senti_ws_negative = pd.read_csv(path + 'functions/SentiWS_v1.8c_Negative.txt', sep = '\t', header = None)
        senti_ws = pd.concat([senti_ws_positive, senti_ws_negative], axis=0, ignore_index=True)
        senti_ws[0] = senti_ws[0].apply(lambda x: x.split('|')[0])
        senti_ws = senti_ws.set_index(0)
        senti_ws = senti_ws[1].to_dict()
        self.senti_ws = pd.concat([senti_ws_positive, senti_ws_negative], axis = 0,ignore_index=True)


    def add_comments(self, comments_list):
        self.comments_list = comments_list.split(' || ')

    def prep_comments(self):
        comments_list = self.comments_list
        comments_list_preped = []
        for comment in comments_list:
            comments_list_preped.append(clean_text(comment))
        self.comments_list_preped = comments_list_preped

    def calc_sentiment_score1(self, txt):
        compare_strings = self.senti_ws.keys()
