class Post:
    def __init__(self, post_image, subscription, full_text):
        self.__post_image = post_image
        self.__subscription = subscription
        self.__full_text = full_text

    def set_image(self, path):
        self.__post_image = path

    def get_image(self):
        return self.__post_image

    def set_subscription(self, subscription):
        self.__subscription = subscription

    def get_subscription(self):
        return self.__subscription

    def set_full_text(self, text):
        self.__full_text = text

    def get_full_text(self):
        return self.__full_text
