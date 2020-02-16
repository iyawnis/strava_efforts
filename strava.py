import logging
import time
import os
from stravalib import Client
from store import get_access_token, get_refresh_token, set_access_token, set_refresh_token
from stravalib.exc import ObjectNotFound

logger = logging.getLogger(__name__)


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URL = os.environ.get("REDIRECT_URL")

TIMEFRAME = {
    'month': 'this_month',
    'year': 'this_year',
    'week': 'this_week',
    'today': 'today'
}

def set_token(token_dict):
    set_access_token(token_dict["access_token"], int(token_dict["expires_at"] - time.time()))
    set_refresh_token(token_dict["refresh_token"])
    return token_dict["access_token"]

def get_token():
    if requires_authorization():
        logger.error("Tried to retrieve token, but user authorization is required")
        raise Exception("User is required to complete authentication")
    access_token, refresh_token = (get_access_token(), get_refresh_token())
    if access_token:
        logger.info("Return stored token")
        return access_token
    logger.info("Retrieving refresh token")
    client = Client()
    token_dict = client.refresh_access_token(CLIENT_ID, CLIENT_SECRET, refresh_token)
    return set_token(token_dict)

def get_client():
    return Client(access_token=get_token())

def get_efforts_for_segment(timeframe, segment_id):
    client = get_client()
    if timeframe not in TIMEFRAME:
        raise ValueError(f'Unknown timeframe option {timeframe}')
    try:
        leaderboard = client.get_segment_leaderboard(segment_id, timeframe=TIMEFRAME[timeframe])
        return leaderboard.effort_count
    except ObjectNotFound:
        logger.exception(f'Invalid segmentId: {segment_id}')
    return None


def requires_authorization():
    access_token, refresh_token = (get_access_token(), get_refresh_token())
    if access_token or refresh_token:
        return False
    return True

def get_authorization_url():
    client = Client()
    return client.authorization_url(client_id=CLIENT_ID, redirect_uri=REDIRECT_URL)

def exchange_code_for_token(code):
    client = Client()
    token_dict = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code)
    return set_token(token_dict)
