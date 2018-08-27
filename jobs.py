from strava import get_efforts_for_segment
from store import set_segment_count, get_segments


def store_count_for_timeframe(timeframe):
    for segment in get_segments():
        effort_count = get_efforts_for_segment(timeframe, segment)
        set_segment_count(timeframe, segment, effort_count)

