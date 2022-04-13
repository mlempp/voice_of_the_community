'''
Autor: Martin Lempp

Kurzbeschreibung:
lade die Thumbnails der videos für den finalen Report
'''
import os
import urllib.request
from tqdm import tqdm
import pandas as pd

def thumbnail_database_update(path):

    #load video_database
    #check for every video if thumbnail exists
    #download if not


    existing_thumbnails = os.listdir(path+'thumbnails/')
    if os.path.isfile(path + 'video_DataBase.csv'):
        df_videos = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        df_videos = df_videos.iloc[::-1]
        ids_videos = list(df_videos.index)
        missing_thumbnails = [x for x in ids_videos if x+'.jpg' not in existing_thumbnails]

        if len(missing_thumbnails) > 0:
            print('update thumbnails')
            for missing in tqdm(missing_thumbnails):
                urllib.request.urlretrieve(f"https://img.youtube.com/vi/{missing}/0.jpg", path+f"thumbnails/{missing}.jpg")

    else:
        print("no database existent, no thumbnails for scrapping")

