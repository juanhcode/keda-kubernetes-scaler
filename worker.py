import redis
import time
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_queue = os.getenv("REDIS_QUEUE", "myqueue")

r = redis.Redis(host=redis_host, port=6379)

print(f"Worker started. Listening on queue: {redis_queue}", flush=True)
while True:
    task = r.blpop(redis_queue, timeout=0)
    if task:
        print(f"Processing task: {task[1].decode('utf-8')}", flush=True)
    time.sleep(1)
