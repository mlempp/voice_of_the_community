'''
Autor: Martin Lempp

Kurzbeschreibung:
Erstellung der Kommentar-Datenbank und update
'''
import pandas as pd
import os
from datetime import datetime as timer
from datetime import date
import json
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")
import googleapiclient.discovery



def load_all_video_comments(video_id, yt):
    response = yt.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat="plainText", pageToken ='').execute()
    comment_list = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response['items']]
    page = 0
    print(f'        comment page: {page}')
    if 'nextPageToken' in response.keys():
        next_page_token = response.get("nextPageToken")
        while next_page_token:
            page+=1
            if page%10 == 0:
                print(f'        comment page: {page}')
            response_new = yt.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat="plainText", pageToken =next_page_token).execute()
            comment_list_new = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response_new['items']]
            comment_list = comment_list+comment_list_new
            if 'nextPageToken' in response_new.keys():
                next_page_token = response_new.get("nextPageToken")
            else:
                next_page_token = None
    return comment_list



def comment_database_update(path):

    with open(path+'api_key.txt') as f:
        lines = f.readlines()
    api_key = lines[0]

    yt = googleapiclient.discovery.build('youtube', 'v3', developerKey = api_key)

    if os.path.isfile(path + 'video_DataBase.csv'):
        df_videos = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        df_videos = df_videos.iloc[::-1]
        if os.path.isfile(path + 'comment_DataBase.json'):

            with open(path+'comment_DataBase.json', 'r') as jsonfile:
                 comment_dict = json.load(jsonfile)

            ids_comments = list(comment_dict.keys())
            ids_videos = list(df_videos.index)

            missing_videos = [x for x in ids_videos if x not in ids_comments]
            last_30_videos = ids_videos[-30:]
            last_30_videos_not_missing = [x for x in last_30_videos if x not in missing_videos]

            videos_for_update = missing_videos+last_30_videos_not_missing
            for video_ID in videos_for_update:
                print(f'    load comments for {df_videos.loc[video_ID].video_title}')
                comments = load_all_video_comments(video_ID, yt)
                print(f'        {len(comments)} comments loaded')
                if video_ID in ids_comments: #update if we have already comments for the video
                    tmp_dct = comment_dict[video_ID]
                    existing_comments = [x['txt'] for x in tmp_dct.values()]
                    new_comments = [x for x in comments if x not in existing_comments]
                    max_id = max([int(x) for x in tmp_dct.keys()])
                    for i,c in enumerate(new_comments):
                        tmp_dct[i+1+max_id] = {}
                        tmp_dct[i+1+max_id]['txt'] = c
                    comment_dict[video_ID] = tmp_dct
                else:
                    comment_dict[video_ID] = {}
                    for i,c in enumerate(comments):
                        comment_dict[video_ID][i] = {}
                        comment_dict[video_ID][i]['txt'] = c

        else:
            print ("no comment database existent...create")
            comment_dict = {}
            for video_ID in df_videos.index:
                print(f'    load comments for {df_videos.loc[video_ID].video_title}')
                comments = load_all_video_comments(video_ID, yt)
                print(f'        {len(comments)} comments loaded')
                comment_dict[video_ID] = {}
                for i,c in enumerate(comments):
                    comment_dict[video_ID][i] = {}
                    comment_dict[video_ID][i]['txt'] = c

        with open('comment_DataBase.json', 'w') as file:
            json.dump(comment_dict, file, indent=4)

    else:
        print("no database existent, no videos for scrapping")

