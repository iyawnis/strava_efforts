from datetime import date
from app import db
from strava import get_segment, get_efforts_for_segment
import logging 
from models import Segment, SegmentEffort

logger = logging.getLogger(__name__)

hardcoded_segments = [
    7550717,
    1184996,
    1444413,
    1552278,
    1329405,
    1087375,
    1164504,
    998208,
    14021755,
    1018221,
    1329459,
    1141197,
    1900485,
    2413551,
    1164862,
    1339119,
    17077459,
    1693611,
    15167428,
    6838005,
    1340567
]

def store_segments_counts():
    today = date.today()
    for segment in Segment.query.all()():
        effort_count, athlete_count = get_efforts_for_segment(segment)
        s = Segment.query.get(segment)
        e = SegmentEffort(effort_count=effort_count, athlete_count=athlete_count, segment=s, date=today)
        db.session.add(e)
    db.session.commit()



def load_segments():
    stored_segments = [s.segment_id for s in Segment.query.all()]

    for new in set(hardcoded_segments) - set(stored_segments):
        segment = get_segment(new)
        import pdb; pdb.set_trace()
        s = Segment(segment_id=new, name=segment.name, created_at=segment.created_at)
        logger.info(f"Creating Segment: {segment.name}")
        db.session.add(s)

    db.session.commit()
