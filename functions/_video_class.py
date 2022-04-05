class video:
    def __init__(self, video_id, video_title):
        self.video_id = video_id
        self.video_title = video_title

    def add_comments(self, comments_list):
        self.comments_list = comments_list