import json

import redis
from flask import request, jsonify

from ActivityUsingFlask.common.libs.helper import calHistoryExchange, getTodayCurSignUpNums, getNowDay, \
    calUserSignUp2LoveNums, getAllLoveNums, getAllDonateNums
from ActivityUsingFlask.web.codis_config import CodisConfig
from ActivityUsingFlask.web.day_donate_person_details import DayDonatePersonDetails
from ActivityUsingFlask.web.dict_to_struct import DictToStruct
from ActivityUsingFlask.web.get_love_nums import getAddSignUpNums
from ActivityUsingFlask.web.homepage import set_default
from . import web


def getCurDayLearnTime(uid):
    # for test
    return 1

def doNateAction(uid, tidList):
    redisKey = CodisConfig().user_detail
    redisCourseKey = CodisConfig().course_detail
    globalDonateDetailsKey = CodisConfig().global_donate_details
    dayDonateCourseNumsKey = CodisConfig().day_donate_course_nums
    dayDonatePersonNumsKey = CodisConfig().day_donate_person_nums
    NINE_MINS = 9 * 60
    nowDay = getNowDay()

    resultCourseTime = 0.0
    resultRestLoveNums = 0.0
    r = redis.Redis(host='localhost', port=6379, db=0)
    userDetails = r.hget(redisKey, str(uid))
    allDonateNums = 0.0
    allDonateCourseNums = 0.0
    userInfoDict = json.loads(userDetails)
    userInfo = DictToStruct(**userInfoDict)
    userDonateRecords = userInfo.donateCourseTimeRecords
    for donateRecord in userDonateRecords:
        allDonateCourseNums += float(donateRecord) * 3
    resultCourseTime = allDonateCourseNums
    curDayLearnTime = getCurDayLearnTime(uid)
    previousLearnTime = userInfo.previousLearnTime
    allLearnTime = previousLearnTime + curDayLearnTime
    userExchangeRecords = userInfo.exchangeLoveNumsRecords
    previousExchangedLoveNums = calHistoryExchange(userInfo)
    learnTime2LoveNums = ((allLearnTime - previousExchangedLoveNums * NINE_MINS) / NINE_MINS)
    userExchangeRecords.append(learnTime2LoveNums)
    userInfo.exchangeLoveNumsRecords = userExchangeRecords
    todayCurSignUpNums = getTodayCurSignUpNums(userInfo, nowDay)
    addSignUpNums = getAddSignUpNums(uid, redisCourseKey)
    todayUpdateSignUpNums = addSignUpNums + todayCurSignUpNums
    userSignUp2LoveNums = calUserSignUp2LoveNums(todayCurSignUpNums, todayUpdateSignUpNums)
    userDaySignUpNums = userInfo.daySignUpNums
    userDaySignUpNums[str(nowDay)] = todayUpdateSignUpNums
    loveNumAddRecords = userInfo.AllloveNumsRecordsList
    loveNumAddRecords.append(userSignUp2LoveNums)
    loveNumAddRecords.append(learnTime2LoveNums)
    userInfo.AllloveNumsRecordsList = loveNumAddRecords
    r.hset(redisKey, uid, json.dumps(userInfo.__dict__, default=set_default))
    allLoveNums = getAllLoveNums(loveNumAddRecords, learnTime2LoveNums, userSignUp2LoveNums)
    allDonateNums = getAllDonateNums(userInfo)
    loveNums = allLoveNums - allDonateNums
    if loveNums < 0:
        return 0.0, 0.0
    courseTime = loveNums / 3
    resultRestLoveNums = loveNums - courseTime * 3
    allDonateCourseNums += courseTime
    userDonateRecords.append(courseTime)
    userInfo.donateCourseTimeRecords = userDonateRecords
    userInfo.latestDonateTime = nowDay
    r.hset(redisKey, uid, json.dumps(userInfo.__dict__, default=set_default))
    if r.exists(globalDonateDetailsKey) == 0:
        globalDonateNums = 0
    else:
        globalDonateNums = int(r.get(globalDonateDetailsKey))
    globalDonateNums += courseTime
    r.set(globalDonateDetailsKey, str(globalDonateNums))
    # 如果哈希表含有给定字段，返回 1 。 如果哈希表不含有给定字段，或 key 不存在，返回 0
    if r.hexists(dayDonateCourseNumsKey, nowDay) == 0:
        r.hset(dayDonateCourseNumsKey, nowDay, '0')
    dayDonateCourseNums = r.hget(dayDonateCourseNumsKey, nowDay)
    dayNums = int(dayDonateCourseNums) + courseTime
    r.hset(dayDonateCourseNumsKey, nowDay, dayNums)
    # 增加每天的捐赠人数统计
    if r.hexists(dayDonatePersonNumsKey, nowDay) == 0:
        dayDonatePersonDetails = DayDonatePersonDetails()
        r.hset(dayDonatePersonNumsKey, nowDay, json.dumps(dayDonatePersonDetails.__dict__, default=set_default))
    dayDonatePersonDetailsBinary = r.hget(dayDonatePersonNumsKey, nowDay)
    dayDonatePersonDetailsDict = json.loads(dayDonatePersonDetailsBinary)
    dayDonatePersonDetails = DictToStruct(**dayDonatePersonDetailsDict)
    dayDonatePersonDetails.uinSet.add(uid)
    r.hset(dayDonatePersonNumsKey, nowDay, json.dumps(dayDonatePersonDetails.__dict__, default=set_default))
    resultCourseTime = allDonateCourseNums
    return resultRestLoveNums, resultCourseTime


@web.route('/getDonateCourseTime')
def donateCourseTimeService():
    uid = request.args['uid']
    # get tidList from zk, here just for test
    tidList = []
    resultRestLoveNums, resultCourseTime = doNateAction(uid, tidList)
    return jsonify({'resultRestLoveNums': resultRestLoveNums, 'resultCourseTime': resultCourseTime})