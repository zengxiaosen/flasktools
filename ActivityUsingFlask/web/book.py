import json

from ActivityUsingFlask.common.libs.helper import is_isbn_or_key
from ActivityUsingFlask.forms.book import SearchForm
from ActivityUsingFlask.view_models.book import BookViewModel, BookCollection
from . import web
from ActivityUsingFlask.spider.yushuBook import YuShuBook
from flask import jsonify, request




@web.route('/book/search')
def search():
    """
    :param q: common key word  isbn
    :param page:
    :return:
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.searchByIsbn(q)
        else:
            yushu_book.searchByKeyWord(q, page)

        books.fill(yushu_book, q)
        # return jsonify(books.__dict__)
        return json.dumps(books, default=lambda o: o.__dict__)
    else:
        return jsonify({'msg': 'params validate failed'})
