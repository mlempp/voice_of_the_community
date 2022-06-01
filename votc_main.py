'''
Autor: Martin Lempp

Kurzbeschreibung:
Hauptprogramm zur Sentimentanalyse und Report-Erstellung
'''
import pandas as pd
import os
from datetime import datetime as timer
from datetime import date,timedelta
import sys
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _generate_update_comment_database import *
from _generate_update_video_database import *
from _helper_functions import *
from _update_thumbnail_database import *
from _comment_analyser import *
# from _video_class import *
# from _defined_past_analysis import *
# from _global_analysis import *
# from _yearly_analysis import *




def main():
    path = os.getcwd() + '/'

    q_update = input('Update data? (yes/no): ').upper()
    if q_update == 'YES':
        video_database_update(path)
        comment_database_update(path)
        thumbnail_database_update(path)


    q_analysis = input('Analyse? (yes/no): ').upper()
    if q_analysis == 'YES':
        df_videos = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        df_videos.video_date = pd.to_datetime(df_videos.video_date)
        df_comments = load_newest_comment_file(path)

        results = {}
        single_analysis = input('Analyse single video? (yes/no): ').upper()
        if single_analysis == 'YES':
            analysis_date = pd.to_datetime(input('which date (DD.MM.YYYY): '), format='%d.%m.%Y')
            vsoi = df_videos[df_videos.video_date.isin([analysis_date])]
            csoi = df_comments[df_comments.VideoID.isin([vsoi.index[0]])]

            analysis_result = analyse_comments(csoi,path)
            results[vsoi.index[0]] = analysis_result

        else:
            multi_analysis = input('Analyse multiple videos? (yes/no): ').upper()
            if multi_analysis == 'YES':
                start_date = input('which starting date (DD.MM.YYYY): ')
                analysis_start_date = pd.to_datetime(start_date, format='%d.%m.%Y')
                end_date = input('which end date (DD.MM.YYYY): ')
                analysis_end_date = pd.to_datetime(end_date, format='%d.%m.%Y')
                analysis_range = pd.date_range(analysis_start_date,analysis_end_date-timedelta(days=1)).to_list()
                vsoi = df_videos[df_videos.video_date.isin(analysis_range)]
                time_line_analysis = input('Analyse as one series? (yes/no) (alternative: all videos by themself): ').upper()
                if time_line_analysis == 'YES':
                    csoi = df_comments[df_comments.VideoID.isin(vsoi.index)]
                    analysis_result = analyse_comments(csoi,path)
                    results[f'{start_date}-{end_date}'] = analysis_result
                else:
                    for i,row in vsoi.iterrows():
                        csoi = df_comments[df_comments.VideoID.isin([i])]
                        analysis_result = analyse_comments(csoi,path)
                        results[i] = analysis_result

        #report analysis

if __name__ == "__main__":
    main()



# #
# for i, row in tqdm(df_comments.iterrows(), total = df_comments.shape[0]):
#     txt = row.comment_preped
#     df_comments.loc[i, 'Sentiment_score_5'] = calc_sentiment_score_from_dict_mean(txt, senti_5_polarity)


