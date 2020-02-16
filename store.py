from datetime import date
import json
import os
import redis as _redis

REDIS_URL = os.environ.get('REDISTOGO_URL')

ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"

redis = _redis.from_url(REDIS_URL)

TIMEFRAME_FORMAT = {
    'today': '%Y%m%d',
    'month': '%Y%m',
    'week': '%Y%V',
    'year': '%Y'
}


def set_access_token(token, ttl):
    redis.set(ACCESS_TOKEN_KEY, token, ex=ttl)


def set_refresh_token(token):
    redis.set(REFRESH_TOKEN_KEY, token)

def get_access_token():
    return redis.get(ACCESS_TOKEN_KEY)


def get_refresh_token():
    return redis.get(REFRESH_TOKEN_KEY)


def set_segment_count(timeframe, segment, count):
    strdate = date.today().strftime(TIMEFRAME_FORMAT[timeframe])
    data = redis.hget(timeframe, segment)
    data = json.loads(data) if data else {}
    data[strdate] = count
    return redis.hset(timeframe, segment, json.dumps(data))


def get_data_for_timeframe(timeframe):
    if timeframe not in TIMEFRAME_FORMAT:
        raise ValueError(f'Invalid timeframe value: {timeframe}')
    data = redis.hgetall(timeframe)
    return {key.decode('utf-8'): json.loads(value) for key, value in data.items()}


def get_segments():
    data = redis.get('segments')
    if not data:
        data = json.dumps([])
    return json.loads(data)


if __name__ == '__main__':
    import pdb; pdb.set_trace()
    print('debug mode')
