
from flaskmvcYushu.httper import HTTP
class YuShuBook:

    isbnUrl = 'http://t.yushu.im/v2/book/isbn/{}'
    keywordUrl = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def searchByIsbn(cls, isbn):
        url = cls.isbnUrl.format(isbn)
        result = HTTP.get(url)
        # dict
        return result
    @classmethod
    def searchByKeyWord(cls, keyword, count=15, start=0):
        url = cls.keywordUrl.format(keyword, count, start)
        result = HTTP.get(url)
        return result