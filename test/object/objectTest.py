import json
from collections import namedtuple

import redis

from ActivityUsingFlask.web.dict_to_struct import DictToStruct


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

class UserDetails:
    def __init__(self):
        self.AllloveNumsRecordsList = []
        self.donateCourseTimeRecords = []
        self.cidSet = set()
        self.previousLearnTime = 0.0
        self.exchangeLoveNumsRecords = []
        self.latestShareTime = ''
        self.latestDonateTime = ''
        self.daySignUpNums = {}
        self.timerTime = []

class CodisConfig:

    def __init__(self):
        self.user_detail = 'USER_DETAIL'

# userDetails = UserDetails()
# userDetails.donateCourseTimeRecords.append('test')
# userDetails.AllloveNumsRecordsList.append('test')
# # arr = [name for name in dir(userDetails) if not name.startswith('__')]
# js = json.dumps(userDetails.__dict__, default=set_default)
# print(js)
# userInfo = json.loads(js)
# print(userInfo)

print(CodisConfig().user_detail)
r = redis.Redis(host='localhost', port=6379, db=0)
userDetails = r.hget('test', 'test')
print(userDetails)
print(type(json.loads(userDetails)))
print(json.dumps(DictToStruct(**json.loads(userDetails)).__dict__))
if userDetails == None:
    print('none')
    userDetails = UserDetails()
    userDetails.donateCourseTimeRecords.append('test')
    userDetails.AllloveNumsRecordsList.append('test')
    userDetails.cidSet.add('test')
    print(userDetails.__dict__)
    r.hset('test', 'test', json.dumps(userDetails.__dict__, default=set_default))

