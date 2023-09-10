import datetime


class Post:
    def __init__(self, post_image, caption, full_text):
        self.post_image = post_image
        self.caption = caption
        self.full_text = full_text
        self.post_date = datetime.datetime.now()
        self.comments = []
        self.views = 0
        self.likes = ''  # users names list

    def get_post_data(self):
        return {'img': self.post_image, 'caption': self.caption, 'full_text': self.full_text,
                'date': self.post_date.strftime('%d/%m/%Y'), 'comments': self.comments, 'views': self.views,
                'likes': self.likes}


class Comment:
    def __init__(self):
        self.author = None
        self.text = None
        self.date = datetime.datetime.now()
