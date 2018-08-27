import logging
import os
from stravalib.client import Client
from stravalib.exc import ObjectNotFound

logger = logging.getLogger(__name__)


ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
TIMEFRAME = {
    'month': 'this_month',
    'year': 'this_year',
    'week': 'this_week',
    'today': 'today'
}

client = Client(access_token=ACCESS_TOKEN)

def get_efforts_for_segment(timeframe, segment_id):
    if timeframe not in TIMEFRAME:
        raise ValueError(f'Unknown timeframe option {timeframe}')
    try:
        leaderboard = client.get_segment_leaderboard(segment_id, timeframe=TIMEFRAME[timeframe])
        return leaderboard.effort_count
    except ObjectNotFound:
        logger.exception(f'Invalid segmentId: {segment_id}')
    return None
