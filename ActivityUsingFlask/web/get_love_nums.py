import json
from collections import namedtuple

from ActivityUsingFlask.common.libs.helper import getNowDay, calHistoryExchange, getTodayCurSignUpNums, \
    calUserSignUp2LoveNums, getAllLoveNums, getAllDonateNums
from ActivityUsingFlask.web.codis_config import CodisConfig
from ActivityUsingFlask.web.course_donate_user_list import CourseDonateUserList
from ActivityUsingFlask.web.dict_to_struct import DictToStruct
from ActivityUsingFlask.web.homepage import set_default
from ActivityUsingFlask.web.user_details import UserDetails
from . import web
from flask import jsonify, request
import redis


def getCurDayLearnTime(uid):
    # for test
    return 1


def getPreviousLearnTime(userInfo):
    previousLearnTime = 0.0
    if userInfo.previousLearnTime != 0.0:
        previousLearnTime = userInfo.previousLearnTime
    return previousLearnTime





def getLearnTime2LoveNums(userInfo, uid):
    NINE_MINS = 9 * 60
    curDayLearnTime = getCurDayLearnTime(uid)
    previousLearnTime = getPreviousLearnTime(userInfo)
    allLearnTime = previousLearnTime + curDayLearnTime
    previousExchangeLoveNums = calHistoryExchange(userInfo)
    learnTime2LoveNums = float((allLearnTime - previousExchangeLoveNums * NINE_MINS) / NINE_MINS)
    return learnTime2LoveNums



def getCourseDetailsList(redisCourseKey):
    # load zk, here is just a test
    tidList = []
    courseDetailsList = []
    r = redis.Redis(host='localhost', port=6379, db=0)
    for tid in tidList:
        courseDetails = r.hget(redisCourseKey, str(tid))
        if courseDetails != None:
            courseDetailsList.append(courseDetails)
        else:
            courseDonateUserLst = CourseDonateUserList()
            courseDonateUserLst.tid = tid
            r.hset(redisCourseKey, str(tid), json.dumps(courseDonateUserLst.__dict__))
    return courseDetailsList


def getUidList(tidDonateUsrList, redisCourseKey):
    courseDonateUserLst = DictToStruct(**json.loads(tidDonateUsrList))
    uidList = courseDonateUserLst.donateUserIdList
    return uidList


def getTid(tidDonateUsrList):
    courseDonateUserLst = DictToStruct(**json.loads(tidDonateUsrList))
    return courseDonateUserLst.tid


def getAddSignUpNums(uid, redisCourseKey):
    addSignUpNums = 0
    courseDetailsList = getCourseDetailsList(redisCourseKey)
    for tidDonateUsrList in courseDetailsList:
        uidList = getUidList(tidDonateUsrList, redisCourseKey)
        tid = getTid(tidDonateUsrList)
        if uid in uidList:
            continue
        # 调用订单rpc判断该用户这门课是不是报名，如果是，则 新增的报名数 addSignUpNums ++
        checkApply = False
        if checkApply == False:
            continue
        addSignUpNums += 1
    return addSignUpNums


def getUserSignUp2LoveNums(userInfo, nowDay, uid, redisCourseKey):
    todayCurSignUpNums = getTodayCurSignUpNums(userInfo, nowDay)
    addSignUpNums = getAddSignUpNums(uid, redisCourseKey)
    todayUpdateSignUpNums = addSignUpNums + todayCurSignUpNums
    userSignUp2LoveNums = calUserSignUp2LoveNums(todayCurSignUpNums, todayUpdateSignUpNums)
    return userSignUp2LoveNums


def getLoveNumsAddRecords(userInfo):
    return userInfo.AllloveNumsRecordsList


def getLoveNums(uid):
    result = 0.0
    redisKey = CodisConfig().user_detail
    redisCourseKey = CodisConfig().course_detail
    r = redis.Redis(host='localhost', port=6379, db=0)
    userDetails = r.hget(redisKey, str(uid))
    if userDetails == None:
        userDetails = UserDetails()
        r.hset(redisKey, str(uid), json.dumps(userDetails.__dict__, default=set_default))
        return float(result)
    nowDay = getNowDay()
    userDetails = r.hget(redisKey, str(uid))
    userInfoDict = json.loads(userDetails)
    userInfo = DictToStruct(**userInfoDict)
    # print(json.dumps(userInfo.__dict__, default=set_default))
    learnTime2LoveNums = getLearnTime2LoveNums(userInfo, uid)
    userSignUp2LoveNums = getUserSignUp2LoveNums(userInfo, nowDay, uid, redisCourseKey)
    loveNumsAddRecords = getLoveNumsAddRecords(userInfo)
    allLoveNums = getAllLoveNums(loveNumsAddRecords, learnTime2LoveNums, userSignUp2LoveNums)
    allDonateNums = getAllDonateNums(userInfo)
    loveNums = allLoveNums - allDonateNums
    if loveNums < 0:
        return 0
    courseTime = loveNums / 3
    result = courseTime
    return result

@web.route('/getLoveNums')
def getLoveNumsService():
    uid = request.args['uid']
    curLoveNums = getLoveNums(uid)
    return curLoveNums