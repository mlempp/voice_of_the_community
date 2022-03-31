'''
Autor: Martin Lempp
Datum: 30.30.2022

Kurzbeschreibung:
Erstellung der Kommentar Datenbank und update

'''
import numpy as np
import pandas as pd
import random

import re
import os
from datetime import datetime as timer
from datetime import date
import pickle
import json
from tqdm import tqdm
import requests
from urllib.request import urlopen
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")
import googleapiclient.discovery



def load_all_video_comments(video_id, yt):
    response = yt.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat="plainText", pageToken ='').execute()
    comment_list = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response['items']]
    next_page_token = response["nextPageToken"]
    count = 0
    while next_page_token:
        count+=1
        print(count)
        response_new = yt.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat="plainText", pageToken =next_page_token).execute()
        comment_list_new = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response['items']]
        comment_list = comment_list+comment_list_new


def comment_database_update():

    path = os.getcwd()+ '\\'


    with open(path+'api_key.txt') as f:
        lines = f.readlines()
    api_key = lines[0]

    yt = googleapiclient.discovery.build('youtube', 'v3', developerKey = api_key)

    if os.path.isfile(path + 'video_DataBase.csv'):
        df_videos = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        if os.path.isfile(path + 'comment_DataBase.csv'):
            print ("comment database existent...update")

            no_comment
        else:
            print ("no comment database existent...create")
            df_comments = pd.DataFrame()
            for video_ID in df_videos.index:
                video_info = pd.Series(name = video_ID)
                comments = load_all_video_comments(video_ID, yt)



                video_info['comments'] =
                df_comments = df_comments.append(video_info)


    else:
        print("no database existent, no videos for scrapping")