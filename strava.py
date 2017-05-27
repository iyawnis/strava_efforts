import os

from stravalib.client import Client
from datetime import datetime

TOKEN = os.environ.get('STRAVA_TOKEN')

def get_segments_effort_count(segment_ids, start_date, end_date):
    client = Client(access_token=TOKEN)
    return {
        segment_id: get_segment_effort_count(segment_id, start_date, end_date, client)
        for segment_id in segment_ids}

def get_segment_effort_count(segment_id, start_date, end_date, client=None):
    if client is None:
        client = Client(access_token=TOKEN)

    segment_efforts = client.get_segment_efforts(
        segment_id,
        start_date_local=start_date,
        end_date_local=end_date)
    return len(list(segment_efforts))