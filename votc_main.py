'''
Autor: Martin Lempp

Kurzbeschreibung:
Hauptprogramm zur Sentimentanalyse und Report-Erstellung

dev V 1.1
'''
import pandas as pd
import os
from datetime import datetime as timer
from datetime import date,timedelta
import sys
from functions._generate_update_comment_database import *
from functions._generate_update_video_database import *
from functions._helper_functions import *
from functions._update_thumbnail_database import *
from functions._comment_analyser import *
from functions._write_report import *
# from _video_class import *
# from _defined_past_analysis import *
# from _global_analysis import *
# from _yearly_analysis import *
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")



def main():
    path = os.getcwd() + '/'

    q_update = input_yes_no('Update data? (yes/no): ')
    if q_update == 'YES':
        video_database_update(path)
        comment_database_update(path)
        thumbnail_database_update(path)


    q_analysis = input_yes_no('Analyse? (yes/no): ')
    if q_analysis == 'YES':
        df_videos = pd.read_csv(path+'video_DataBase.csv', sep = ';', index_col = 0)
        df_videos.video_date = pd.to_datetime(df_videos.video_date)
        df_comments = load_newest_comment_file(path)

        results = {}
        single_analysis = input_yes_no('Analyse single video? (yes/no): ')
        if single_analysis == 'YES':
            analysis_date = pd.to_datetime(input('which date (DD.MM.YYYY): '), format='%d.%m.%Y')
            vsoi = df_videos[df_videos.video_date.isin([analysis_date])]
            csoi = df_comments[df_comments.VideoID.isin([vsoi.index[0]])]

            analysis_result = analyse_comments(csoi,path)
            results[vsoi.video_title.iloc[0]] = analysis_result

        else:
            multi_analysis = input_yes_no('Analyse multiple videos? (yes/no): ')
            if multi_analysis == 'YES':
                analysis_start_date = input_date('which starting date (DD.MM.YYYY): ')
                analysis_end_date = input_date('which end date (DD.MM.YYYY): ')
                analysis_range = pd.date_range(analysis_start_date,analysis_end_date).to_list()
                vsoi = df_videos[df_videos.video_date.isin(analysis_range)]
                time_line_analysis = input_yes_no('Analyse as one series? (yes/no) (alternative: all videos by themself): ')

                if time_line_analysis == 'YES':
                    csoi = df_comments[df_comments.VideoID.isin(vsoi.index)]
                    analysis_result = analyse_comments(csoi,path)
                    results[f'{analysis_start_date}-{analysis_end_date}'] = analysis_result
                else:
                    for i,row in vsoi.iterrows():
                        csoi = df_comments[df_comments.VideoID.isin([i])]
                        analysis_result = analyse_comments(csoi,path)
                        results[row.video_title] = analysis_result

        report = generate_report(results)
        with open(path + f"output/analysis_{d}.html", "w", encoding='utf-8') as f:
            f.write(report)

if __name__ == "__main__":
    main()



#
# import time
#
# t0 = time.time()
#
# code
#
# t1 = time.time()
# total = t1-t0
# print(total)
#
#
# df_comments[['Sentiment_score_1','Sentiment_score_6','Sentiment_score_9','Sentiment_score_12']] = df_comments.apply(lambda x: calc_sentiment_scores_from_dict(x.comment_preped, dct = senti_1_ws),axis = 1, result_type="expand")
# df_comments[['Sentiment_score_4','Sentiment_score_7','Sentiment_score_10','Sentiment_score_13']] = df_comments.apply(lambda x: calc_sentiment_scores_from_dict(x.comment_preped, dct = senti_4_polarity),axis = 1, result_type="expand")
# df_comments[['Sentiment_score_5','Sentiment_score_8','Sentiment_score_11','Sentiment_score_14']] = df_comments.apply(lambda x: calc_sentiment_scores_from_dict(x.comment_preped, dct = senti_5_polarity),axis = 1, result_type="expand")
#
#
#
# df_comments.to_csv(path + d2 + '_comment_DataBase.csv', sep=';')

