from flask import Blueprint

web = Blueprint('web', __name__)

from flaskmvcYushu.web import book
from flaskmvcYushu.web import user