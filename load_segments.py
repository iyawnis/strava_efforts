from app import db
from models import Segment
from strava import get_segment

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

stored_segments = [s.segment_id for s in Segment.query.all()]

for new in set(hardcoded_segments) - set(stored_segments):
    segment = get_segment(new)
    db.session.add(Segment(segment_id=new, name=segment.name, created_at=segment.created_at))

db.session.commit()
