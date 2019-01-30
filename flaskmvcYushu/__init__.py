# __init__.py means make a package to a python package and do some init thing
from flask import Flask
from sqlalchemy import create_engine


def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    return app

def create_egn():
    engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/test', encoding="utf-8")
    return engine

def register_blueprint(app):
    from flaskmvcYushu.web.book import web
    app.register_blueprint(web)
