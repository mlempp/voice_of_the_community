path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _helper_functions import *

class video:
    def __init__(self, video_id, video_title, video_date):
        self.video_id = video_id
        self.video_title = video_title
        self.video_date = video_date


    def add_comments(self, comments_list):
        self.comments_list = comments_list.split(' || ')

    def prep_comments(self):
        comments_list = self.comments_list
        comments_list_preped = []
        for comment in comments_list:
            comments_list_preped.append(clean_text(comment))
        self.comments_list_preped = comments_list_preped
