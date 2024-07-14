from datetime import datetime
import time

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(now)

start = time.time()
print("hello")
time.sleep(10)
end = time.time()
print(end - start)