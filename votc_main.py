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

comment_dict_new = {}
for vid in comment_dict.keys():
     vid_dict = comment_dict[vid]
     comment_dict_new[vid] = {}
     for comment in vid_dict.keys():
         comment_dict_new[vid][comment] = {}
         comment_dict_new[vid][comment]['txt'] = vid_dict[comment]['txt']
         comment_dict_new[vid][comment]['txt_preped'] = vid_dict[comment]['txt_preped']

         comment_dict_new[vid][comment]['score3_preped'] = get_sentiment_score3(vid_dict[comment]['txt_preped'])
         comment_dict_new[vid][comment]['score3'] = get_sentiment_score3(vid_dict[comment]['txt_preped'])
