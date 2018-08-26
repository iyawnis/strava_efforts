import os
import redis

REDIS_URL = os.environ.get('REDISTOGO_URL')

client = redis.from_url(REDIS_URL)


