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
from _helper_functions import *
from tqdm import tqdm
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")
d2 = date.today().strftime("%y%m%d")
import googleapiclient.discovery
path = os.getcwd() + '/'


senti_1_ws_positive = pd.read_csv(path + 'functions/SentiWS_v1.8c_Positive.txt', sep='\t', header=None)
senti_1_ws_negative = pd.read_csv(path + 'functions/SentiWS_v1.8c_Negative.txt', sep='\t', header=None)
senti_1_ws = pd.concat([senti_1_ws_positive, senti_1_ws_negative], axis=0, ignore_index=True)
senti_1_ws[0] = senti_1_ws[0].apply(lambda x: x.split('|')[0])
senti_1_ws = senti_1_ws.set_index(0)
senti_1_ws = senti_1_ws[1].to_dict()

senti_4_polarity = pd.read_csv(path + 'functions/train_test_lemma_polarity.txt', sep='\t', header=None)
senti_4_polarity[0] = senti_4_polarity[0].apply(lambda x: x.split('_')[0])
senti_4_polarity = senti_4_polarity.set_index(0).replace({'NEG':-1,'POS':1, 'NEU': 0, 'INT': 0, 'SHI': 0 })
senti_4_polarity = senti_4_polarity[1].to_dict()


def load_all_video_comments(video_id, yt):
    response = yt.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat="plainText", pageToken ='').execute()
    comment_list = [(item["snippet"]["topLevelComment"]["id"], item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]) for item in response['items']]
    page = 0
    print(f'        comment page: {page}')
    if 'nextPageToken' in response.keys():
        next_page_token = response.get("nextPageToken")
        while next_page_token:
            page+=1
            if page%10 == 0:
                print(f'        comment page: {page}')
            response_new = yt.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat="plainText", pageToken =next_page_token).execute()
            comment_list_new = [(item["snippet"]["topLevelComment"]["id"], item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]) for item in response_new['items']]
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
        #load video database
        df_videos = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        df_videos = df_videos.iloc[::-1]
        if any(['comment_DataBase' in x for x in os.listdir(path)]):
            print ("comment database existent...update")

            #load comment database
            comment_files = [x for x in os.listdir(path) if 'comment_DataBase' in x]
            comment_files.sort()
            comment_file = comment_files[-1]
            df_comments = pd.read_csv(path+comment_file, sep = ';', index_col = 0, )

            #define videos for update
            ids_comments = list(df_comments.VideoID.unique())
            ids_videos = list(df_videos.index)
            missing_videos = [x for x in ids_videos if x not in ids_comments]
            last_30_videos = ids_videos[-50:]
            last_30_videos_not_missing = [x for x in last_30_videos if x not in missing_videos]
            videos_for_update = missing_videos+last_30_videos_not_missing

            #update videos
            for video_ID in videos_for_update:
                print(f'    load comments for {df_videos.loc[video_ID].video_title}')
                comments = load_all_video_comments(video_ID, yt)
                print(f'        {len(comments)} comments loaded')
                if video_ID in ids_comments: #update if we have already comments for the video
                    tmp_comment_df = df_comments[df_comments.VideoID == video_ID].copy()
                    existing_comments = tmp_comment_df.comment_ID.tolist()
                    new_comment_ids = [x[0] for x in comments if x[0] not in existing_comments]
                    new_comments = [x for x in comments if x[0] in new_comment_ids]
                    for i,c in tqdm(enumerate(new_comments)):
                        comment_series = pd.Series(data = {'VideoID':  video_ID, 'comment_ID': c[0], 'comment': c[1], 'comment_preped': clean_text(c[1])})
                        comment_series['Sentiment_score_1'] = calc_sentiment_score_from_dict_mean(comment_series.comment_preped,senti_1_ws)
                        comment_series['Sentiment_score_2'] = calc_sentiment_score2(comment_series.comment)
                        comment_series['Sentiment_score_3'] = calc_sentiment_score3(comment_series.comment_preped)
                        comment_series['Sentiment_score_4'] = calc_sentiment_score_from_dict_mean(comment_series.comment_preped,senti_4_polarity)
                        df_comments = df_comments.append(comment_series, ignore_index=True)
                else:
                    for i,c in tqdm(enumerate(comments)):   #add all comments if we dont have the video
                        comment_series = pd.Series(data = {'VideoID':  video_ID, 'comment_ID': c[0], 'comment': c[1], 'comment_preped': clean_text(c[1])})
                        comment_series['Sentiment_score_1'] = calc_sentiment_score_from_dict_mean(comment_series.comment_preped,senti_1_ws)
                        comment_series['Sentiment_score_2'] = calc_sentiment_score2(comment_series.comment)
                        comment_series['Sentiment_score_3'] = calc_sentiment_score3(comment_series.comment_preped)
                        comment_series['Sentiment_score_4'] = calc_sentiment_score_from_dict_mean(comment_series.comment_preped,senti_4_polarity)
                        df_comments = df_comments.append(comment_series, ignore_index=True)

        else:
            print ("no comment database existent...create")
            df_comments = pd.DataFrame(columns = ['VideoID', 'comment_ID', 'comment', 'comment_preped', 'Sentiment_score_1', 'Sentiment_score_2', 'Sentiment_score_3'])
            for video_ID in df_videos.index:
                print(f'    load comments for {df_videos.loc[video_ID].video_title}')
                comments = load_all_video_comments(video_ID, yt)
                print(f'        {len(comments)} comments loaded')
                for i,c in tqdm(enumerate(comments)):
                    comment_series = pd.Series(data = {'VideoID':  video_ID, 'comment_ID': c[0], 'comment': c[1], 'comment_preped': clean_text(c[1])})
                    comment_series['Sentiment_score_1'] = calc_sentiment_score_from_dict_mean(comment_series.comment_preped,senti_1_ws)
                    comment_series['Sentiment_score_2'] = calc_sentiment_score2(comment_series.comment)
                    comment_series['Sentiment_score_3'] = calc_sentiment_score3(comment_series.comment_preped)
                    comment_series['Sentiment_score_4'] = calc_sentiment_score_from_dict_mean(comment_series.comment_preped,senti_4_polarity)
                    df_comments = df_comments.append(comment_series, ignore_index=True)

        df_comments.to_csv(path+d2+'_comment_DataBase.csv', sep = ';')
    else:
        print("no database existent, no videos for scrapping")

