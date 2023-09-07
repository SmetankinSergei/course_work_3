import datetime


class Post:
    def __init__(self, post_image, caption, full_text):
        self.__post_image = post_image
        self.__caption = caption
        self.__full_text = full_text
        self.__post_date = datetime.datetime.now()
        self.__comments = []
        self.__likes = []  # users names list

    def get_post_data(self):
        return {'img': self.__post_image, 'caption': self.__caption, 'full_text': self.__full_text,
                'date': self.__post_date.strftime('%d/%m/%Y'), 'comments': self.__comments, 'likes': self.__likes}

    def set_image(self, path):
        self.__post_image = path

    def get_image(self):
        return self.__post_image

    def set_subscription(self, caption):
        self.__caption = caption

    def get_subscription(self):
        return self.__caption

    def set_full_text(self, text):
        self.__full_text = text

    def get_full_text(self):
        return self.__full_text


class Comment:
    def __init__(self):
        self.__author = None
        self.__text = None
        self.__date = datetime.datetime.now()

    def set_author(self, author):
        self.__author = author

    def get_author(self):
        return self.__author

    def set_text(self, text):
        self.__text = text

    def get_text(self):
        return self.__text
