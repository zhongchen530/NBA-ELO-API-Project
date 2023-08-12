import os
import redis
redis_host = os.environ.get("REDIS_HOST","redis")
redis_port = 6379
redis_conn = redis.Redis(host=redis_host,port=redis_port,db=1)