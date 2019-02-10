import json

from ActivityUsingFlask.web.course_donate_user_list import CourseDonateUserList

courseDonateUserLst = CourseDonateUserList()
courseDonateUserLst.tid = 1.0
print(json.dumps(courseDonateUserLst.__dict__))