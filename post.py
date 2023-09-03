class Post:
    def __init__(self, post_image, caption, full_text):
        self.__post_image = post_image
        self.__caption = caption
        self.__full_text = full_text
        self.__likes = []  # users names list
        self.__post_date = None

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
