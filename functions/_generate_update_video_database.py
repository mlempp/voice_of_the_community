'''
Autor: Martin Lempp
Datum: 30.30.2022

Kurzbeschreibung:
Erstellung der Video Datenbank und update

'''
import pandas as pd
import os
from datetime import datetime as timer
from datetime import date
import json
from tqdm import tqdm
import requests
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")


class YTstats:
    '''credits: https://github.com/python-engineer/youtube-analyzer/blob/master/yt_stats.py'''

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def extract_all(self):
        self.get_channel_statistics()
        self.get_channel_video_data()

    def get_channel_statistics(self):
        """Extract the channel statistics"""
        print('get channel statistics...')
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        pbar = tqdm(total=1)

        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0]['statistics']
        except KeyError:
            print('Could not get channel statistics')
            data = {}

        self.channel_statistics = data
        pbar.update()
        pbar.close()
        return data

    def get_channel_video_data(self, limit = None):
        "Extract all video information of the channel"
        print('get video data...')
        channel_videos, channel_playlists = self._get_channel_content(limit=limit)

        parts = ["snippet", "statistics", "contentDetails", "topicDetails"]
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)

        self.video_data = channel_videos
        return channel_videos

    def _get_single_video_data(self, video_id, part):
        """
        Extract further information for a single video
        parts can be: 'snippet', 'statistics', 'contentDetails', 'topicDetails'
        """

        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        return data

    def _get_channel_content(self, limit=None, check_all_pages=True):
        """
        Extract all videos and playlists, can check all available search pages
        channel_videos = videoId: title, publishedAt
        channel_playlists = playlistId: title, publishedAt
        return channel_videos, channel_playlists
        """
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

        vid, pl, npt = self._get_channel_content_per_page(url)
        idx = 0
        while (check_all_pages and npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            next_vid, next_pl, npt = self._get_channel_content_per_page(nexturl)
            vid.update(next_vid)
            pl.update(next_pl)
            idx += 1

        return vid, pl

    def _get_channel_content_per_page(self, url):
        """
        Extract all videos and playlists per page
        return channel_videos, channel_playlists, nextPageToken
        """
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        channel_playlists = dict()
        if 'items' not in data:
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, channel_videos, None

        nextPageToken = data.get("nextPageToken", None)

        item_data = data['items']
        for item in item_data:
            try:
                kind = item['id']['kind']
                published_at = item['snippet']['publishedAt']
                title = item['snippet']['title']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = {'publishedAt': published_at, 'title': title}
                elif kind == 'youtube#playlist':
                    playlist_id = item['id']['playlistId']
                    channel_playlists[playlist_id] = {'publishedAt': published_at, 'title': title}
            except KeyError as e:
                print('Error! Could not extract data from item:\n', item)

        return channel_videos, channel_playlists, nextPageToken

    def dump(self):
        """Dumps channel statistics and video data in a single json file"""
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return

        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,
                                        "video_data": self.video_data}}

        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(" ", "_").lower()
        filename = channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(fused_data, f, indent=4)

        print('file dumped to', filename)


def videos_to_frame(video_dct):

    df = pd.DataFrame(index = video_dct.keys())
    df['video_title'] = [video_dct[x]['title'] for x in video_dct]
    df['video_date'] = [video_dct[x]['publishedAt'] for x in video_dct]
    df['channel'] = [video_dct[x]['channelId'] for x in video_dct]
    df['video_date'] = pd.to_datetime(df.video_date).dt.date
    return df

def video_database_update(path):

    with open(path+'api_key.txt') as f:
        lines = f.readlines()
    api_key = lines[0]

    with open(path+'channel_id.txt') as f:
        lines = f.readlines()
    channel_id = lines[0]

    yt = YTstats(api_key, channel_id)
    if os.path.isfile(path + 'video_DataBase.csv'):
        print ("video database exist...update")
        df_old = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        video_data_new = yt.get_channel_video_data(limit = 3)
        df_new =videos_to_frame(video_data_new)
        df_new_red = df_new[~df_new.index.isin(df_old.index)]
        df = pd.concat([df_new_red,df_old])

    else:
        print ("no video database existent...create")
        video_data_new = yt.get_channel_video_data(limit = 500)
        df = videos_to_frame(video_data_new)

    df.to_csv(path+'video_DataBase.csv', sep = ';')






