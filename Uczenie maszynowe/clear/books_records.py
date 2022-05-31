

class BookRecord:
    def __init__(self, wiki_id, db_id, title, author, publication_date, categories: dict, description):
        self.__wiki_id = wiki_id
        self.__db_id = db_id
        self.__title = title
        self.__author = author
        self.__pub_date = publication_date
        self.__categories = categories
        self.__desc = description

    @property
    def wikipedia_id(self):
        return self.__wiki_id

    @property
    def database_id(self):
        return self.__db_id

    @property
    def publication_date(self):
        return self.__pub_date

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def categories(self):
        return [self.__categories[key] for key in self.__categories]

    @property
    def description(self):
        return self.__desc


