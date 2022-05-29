import pandas as pd
import os
from tqdm import tqdm
from collections import Counter
path = os.getcwd() + '/'
from _video_class import *
from datetime import datetime as timer
from datetime import date
import json
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")


def _global_analysis(path, save_word_count = True):


    pass