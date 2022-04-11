import os
import sys
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _helper_functions import *
import pandas as pd
from collections import Counter

class video:
    def __init__(self, video_id, video_title, video_date, path):
        self.video_id = video_id
        self.video_title = video_title
        self.video_date = video_date
        self.path = path


    def add_comments(self, comments_list):
        '''add the comments for the video from the comment DB and save the word count
        '''
        self.comments_list = comments_list.split(' || ')
        flat_list =  [x.split() for x in self.comments_list]
        all_words = [ item for elem in flat_list for item in elem]
        self.word_count = dict(Counter(all_words))


    def prep_comments(self):
        '''
        prep the comments with helper function clean_text save the word count
        :return:
        '''
        comments_list = self.comments_list
        comments_list_preped = []
        for comment in comments_list:
            comments_list_preped.append(clean_text(comment))
        self.comments_list_preped = comments_list_preped
        flat_list =  [x.split() for x in comments_list_preped]
        all_words = [ item for elem in flat_list for item in elem]
        self.word_count_preped = dict(Counter(all_words))


    def load_sentiment_ws_1(self):
        '''
        load sentimentWS dataframe from https://www.kaggle.com/datasets/rtatman/german-sentiment-analysis-toolkit
        :return:
        '''
        path = self.path
        senti_ws_positive = pd.read_csv(path + 'functions/SentiWS_v1.8c_Positive.txt', sep = '\t', header = None)
        senti_ws_negative = pd.read_csv(path + 'functions/SentiWS_v1.8c_Negative.txt', sep = '\t', header = None)
        senti_ws = pd.concat([senti_ws_positive, senti_ws_negative], axis=0, ignore_index=True)
        senti_ws[0] = senti_ws[0].apply(lambda x: x.split('|')[0])
        senti_ws = senti_ws.set_index(0)
        senti_ws = senti_ws[1].to_dict()
        self.senti_ws = pd.concat([senti_ws_positive, senti_ws_negative], axis = 0,ignore_index=True)


    def calc_sentiment_score1(self, txt):
        self.load_sentiment_ws_1()
        # compare_strings = self.senti_ws.keys()


    def calc_sentiment_score2(self, model):
        self.sentiment_score2 = model.predict_sentiment(self.comments_list)
        self.sentiment_score2_preped = model.predict_sentiment(self.comments_list_preped)
