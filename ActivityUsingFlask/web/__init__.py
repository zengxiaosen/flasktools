from flask import Blueprint
from flask import request, app
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired
web = Blueprint('web', __name__)

from ActivityUsingFlask.web import book
from ActivityUsingFlask.web import user
from ActivityUsingFlask.web import homepage
from ActivityUsingFlask.web import get_love_nums
from ActivityUsingFlask.web import donate_course_time

