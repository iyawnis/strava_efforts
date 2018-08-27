from datetime import date
import json
import os
import redis as _redis

REDIS_URL = os.environ.get('REDISTOGO_URL')

redis = _redis.from_url(REDIS_URL)


def set_segment_count(timeframe, segment, count):
    strdate = date.today().strftime('%Y%m%d')
    data = redis.hget(timeframe, segment)
    if not data:
        data = json.dumps({})
    data = json.loads(data)
    data[strdate] = count
    return redis.hset(timeframe, segment, json.dumps(data))


def get_segments():
    data = redis.get('segments')
    if not data:
        data = json.dumps([])
    return json.loads(data)


if __name__ == '__main__':
    import pdb; pdb.set_trace()
    print('debug mode')
