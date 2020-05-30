import os
import redis as _redis

REDIS_URL = os.environ.get('REDISTOGO_URL')

ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"

redis = _redis.from_url(REDIS_URL)


def set_access_token(token, ttl):
    redis.set(ACCESS_TOKEN_KEY, token, ex=ttl)


def set_refresh_token(token):
    redis.set(REFRESH_TOKEN_KEY, token)

def get_access_token():
    return redis.get(ACCESS_TOKEN_KEY)


def get_refresh_token():
    return redis.get(REFRESH_TOKEN_KEY)


if __name__ == '__main__':
    import pdb; pdb.set_trace()
    print('debug mode')