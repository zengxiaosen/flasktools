import datetime
import time
import pytz
curDay = time.strftime('%Y-%m-%d', time.localtime(time.time()))
print(curDay)

tz = pytz.timezone('Asia/Shanghai')
curTime = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
print(curTime)