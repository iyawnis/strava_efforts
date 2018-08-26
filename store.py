import os
import redis as _redis

REDIS_URL = os.environ.get('REDISTOGO_URL')

redis = _redis.from_url(REDIS_URL)

def set_segment_date_count(segment, date, count):
    hkey = f'segment.{segment}'
    key = date.strftime('%Y%m%d')
    return redis.hset(hkey, key, count)

def get_stored_segments():
    res = redis.scan(0, 'segment.*')
    if len(res) == 2:
        return res[1]
    return None

