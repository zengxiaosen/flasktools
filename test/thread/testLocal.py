import threading
import time
from werkzeug.local import Local

class A:
    b = 1

my_obj = A()
local_obj = Local()
local_obj.b = 1

def worker():
    my_obj.b = 2
    local_obj.b = 2
    print('in new thread local_obj is: ' + str(local_obj.b))

new_t = threading.Thread(target=worker, name='test_thread')
new_t.start()
time.sleep(1)

print(my_obj.b)
print('in main thread local_obj is: ' + str(local_obj.b))