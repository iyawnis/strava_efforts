import os

from stravalib.client import Client
from datetime import datetime

TOKEN = os.environ.get('STRAVA_TOKEN')

def get_segments_effort_count(segment_ids, start_date, end_date):
    client = Client(access_token=TOKEN)
    results = {}
    for segment_id in segment_ids:
        efforts = get_segment_effort_count(segment_id, start_date, end_date, client)
        name = '{} ({})'.format(efforts[0], segment_id)
        results[name] = efforts[1]
    return results

def get_segment_effort_count(segment_id, start_date, end_date, client=None):
    if client is None:
        client = Client(access_token=TOKEN)

    segment_efforts = client.get_segment_efforts(
        segment_id,
        start_date_local=start_date,
        end_date_local=end_date)
    all_efforts = list(segment_efforts)
    if all_efforts:
        segment_name = all_efforts[0].name
        return (segment_name, len(all_efforts),)
    return ('', 0,)