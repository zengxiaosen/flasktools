from flask import Flask, current_app, Request, request

app = Flask(__name__)
# Flask AppContext
# Request RequestContext

# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config['DEBUG']
# ctx.pop()

# with

with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']

# example: file io
# try:
#     f = open(r'/home/aonezeng/a.txt')
#     print(f.read())
# finally:
#     f.close()
#
# with open(r'/home/aonezeng/a.txt') as f:
#     print(f.read())


class MyResource:
    def __enter__(self):
        print('connect to resource')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('process exception')
        else:
            print('no exception')
        print('close resource connection')
        return True

    def query(self):
        print('query data')


try:
    with MyResource() as resource:
        1/0
        resource.query()
except Exception as ex:
    pass
