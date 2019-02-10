import threading
import time

from flask import Request

request = None

request1 = Request()
request2 = Request()
request3 = Request()

# MultiThread
# request = {thread_key1:Request1, ... }

def worker():
    request = Request()
    print('i am thread')
    t1 = threading.current_thread()
    time.sleep(3)
    print(t1.getName())



new_t = threading.Thread(target=worker,name='test_thread')
new_t.start()
new_t = threading.Thread(target=worker,name='test_thread')
new_t.start()
new_t = threading.Thread(target=worker,name='test_thread')
new_t.start()

request

t = threading.current_thread()
print(t.getName())