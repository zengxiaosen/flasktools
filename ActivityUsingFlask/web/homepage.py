import json

from ActivityUsingFlask.web.codis_config import CodisConfig
from ActivityUsingFlask.web.user_details import UserDetails
from . import web
from flask import jsonify, request
import redis

@web.route('/getHomePageInfo')
def getHomePageInfoService():
    uid = request.args['uid']
    if uid != 0:
        addUser(uid)
    allRaiseCourseTimeNums = getAllRaiseNums()
    return jsonify({'allRaiseCourseTimeNums': allRaiseCourseTimeNums})


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def addUser(uid):
    redisKey = CodisConfig().user_detail
    r = redis.Redis(host='localhost', port=6379, db=0)
    userDetails = r.hget(redisKey, str(uid))
    if userDetails == None:
        userDetails = UserDetails()
        r.hset(redisKey, str(uid), json.dumps(userDetails.__dict__, default=set_default))


def getAllRaiseNums():
    redisKey = CodisConfig().global_donate_details
    res = 0.0
    r = redis.Redis(host='localhost', port=6379, db=0)
    if r.get(redisKey) == None:
        return res
    else:
        return float(r.get(redisKey))


