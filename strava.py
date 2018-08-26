import os
from stravalib.client import Client


ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
TIMEFRAME = {
    'MONTH': 'this_month',
    'YEAR': 'this_year',
    'WEEK': 'this_week',
    'TODAY': 'today'
}

def get_efforts_for_segment(segment_id):
    client = Client(access_token=ACCESS_TOKEN)
    leaderboard = client.get_segment_leaderboard(segment_id, timeframe=TIMEFRAME['MONTH'])
    if leaderboard:
        return leaderboard.effort_count
    return None
