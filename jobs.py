from strava import get_efforts_for_segment
from store import set_segment_count, get_segments
from datetime import date


def store_segments_counts():
    from app import db
    from models import Segment, SegmentEffort
    today = date.today()
    for segment in Segment.query.all()():
        effort_count, athlete_count = get_efforts_for_segment(segment)
        s = Segment.query.get(segment)
        e = SegmentEffort(effort_count=effort_count, athlete_count=athlete_count, segment=s, date=today)
        db.session.add(e)
    db.session.commit()
