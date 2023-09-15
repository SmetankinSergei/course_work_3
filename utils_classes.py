class SearchSession:
    def __init__(self):
        self.__items = []
        self.__id_for_start = 1
        self.__has_more = False

    def add_item(self, item):
        self.__items.append(item)

    def get_items_list(self):
        return self.__items

    def set_id_for_start(self, id_for_start):
        self.__id_for_start = id_for_start

    def get_id_for_start(self):
        return self.__id_for_start

    def set_has_more(self, has_more):
        self.__has_more = has_more

    def has_more(self):
        return self.__has_more
