# __init__.py means make a package to a python package and do some init thing
from flask import Flask
from sqlalchemy import create_engine
from ActivityUsingFlask.models.book import db
from ActivityUsingFlask import config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/fisher'
    register_blueprint(app)
    db.init_app(app)

    # load model to db
    # db.create_all(app=app)
    with app.app_context():
        db.create_all()
    return app

def create_egn():
    engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/fisher', encoding="utf-8")
    return engine

def register_blueprint(app):
    from ActivityUsingFlask.web.book import web
    app.register_blueprint(web)

app1 = create_app()