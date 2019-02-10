
from ActivityUsingFlask.common.libs.httper import HTTP


class YuShuBook:

    isbnUrl = 'http://t.yushu.im/v2/book/isbn/{}'
    keywordUrl = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []


    def searchByIsbn(self, isbn):
        url = self.isbnUrl.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)
        return result

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.total = data['books']

    def searchByKeyWord(self, keyword, page=1):
        # current_app.config['PER_PAGE']: default 15
        url = self.keywordUrl.format(keyword, 3, self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)
        return result

    def calculate_start(self, page):
        #  current_app.config['PER_PAGE']: default 15
        return (page-1) * 3
