from flaskmvcYushu.common.libs.helper import is_isbn_or_key
from . import web
from flaskmvcYushu.yushuBook import YuShuBook
from flask import jsonify




@web.route('/book/search/<q>/<page>')
def search(q, page):
    """
    :param q: common key word  isbn
    :param page:
    :return:
    """
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = YuShuBook.searchByIsbn(q)
    else:
        result = YuShuBook.searchByKeyWord(q)
    print(result)
    return jsonify(result)
    # return result
    pass