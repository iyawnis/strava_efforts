from strava import get_efforts_for_segment
from store import set_segment_count, get_segments


def store_segments_counts():
    for segment in get_segments():
        effort_count, athlete_count = get_efforts_for_segment(segment)
        set_segment_count(segment, effort_count, athelete_count)

