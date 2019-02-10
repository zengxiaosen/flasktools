import time
import datetime
import time
import pytz

def is_isbn_or_key(word):
    """
        q common isbn
        page
        :return:
        """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'

    if '-' in word and len(word.replace('-', '')) == 10 and word.replace('-', '').isdigit:
        isbn_or_key = 'isbn'

    return isbn_or_key

def getNowDay():
    curDay = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    tz = pytz.timezone('Asia/Shanghai')
    curTime = datetime.datetime.now(tz).strftime("%Y-%m-%d")
    print(curTime)
    return curTime

def calHistoryExchange(userInfo):
    sum = 0.0
    if userInfo.exchangeLoveNumsRecords == None:
        return 0.0
    for exchangeRecord in userInfo.exchangeLoveNumsRecords:
        sum += float(exchangeRecord)
    return sum

def getTodayCurSignUpNums(userInfo, nowDay):
    todayCurSignUpNums = 0
    curDaySignUpNums = userInfo.daySignUpNums
    if curDaySignUpNums.get(nowDay) != None:
        todayCurSignUpNums = curDaySignUpNums.get(nowDay)
    return todayCurSignUpNums

def calUserSignUp2LoveNums(todayCurSignUpNums, todayUpdateSignUpNums):
    userSignUp2LoveNums = 0
    if todayCurSignUpNums >= 3:
        userSignUp2LoveNums = 0
    else:
        if todayUpdateSignUpNums >=3:
            userSignUp2LoveNums = 3 - todayCurSignUpNums
        else:
            userSignUp2LoveNums = todayUpdateSignUpNums - todayCurSignUpNums
    return userSignUp2LoveNums

def getAllLoveNums(loveNumsAddRecords, learnTime2LoveNums, userSignUp2LoveNums):
    allLoveNums = 0
    for loveNumsRecord in loveNumsAddRecords:
        allLoveNums += loveNumsRecord
    allLoveNums += learnTime2LoveNums
    allLoveNums += userSignUp2LoveNums
    return allLoveNums

def getAllDonateNums(userInfo):
    allDonateNums = 0.0
    for donateRecord in userInfo.donateCourseTimeRecords:
        allDonateNums += float(donateRecord) * 3
    return allDonateNums