
import pandas as pd
import os
from datetime import datetime as timer
from datetime import date
import sys
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")
path = os.getcwd() + '\\'
sys.path.insert(0, path + '/functions/')
from _generate_update_comment_database import *
from _generate_update_video_database import *
from _video_class import *


def main():
    video_database_update()
    comment_database_update()

    global_analysis()
    yearly_analysis(year = 2019)
    defined_past_analysis(delta='14d')

    pass