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
    segments = Segment.query.all()
    logger.info(f"Retrieving segment counts for {len(segments)} segments")
    for segment in segments:
        if SegmentEffort.query.filter_by(segment=segment, date=today).scalar() is not None:
            logger.info(f"Day already collected for {segment.id}, skipping...")
            continue
        effort_count, athlete_count = get_efforts_for_segment(segment.id)
        e = SegmentEffort(effort_count=effort_count, athlete_count=athlete_count, segment=segment, date=today)
        db.session.add(e)
    db.session.commit()
    logger.info("Retrieving counts complete")



def load_segments():
    stored_segments = [s.id for s in Segment.query.all()]
    new_segments = set(hardcoded_segments) - set(stored_segments)
    if new_segments:
        logger.info("Begin loading new segments")
    else:
        logger.info("No new segments to load")
    for segment_id in new_segments:
        segment = get_segment(segment_id)
        s = Segment(id=segment_id, name=segment.name, created_at=segment.created_at.date())
        logger.info(f"Creating Segment: {segment.name}")
        db.session.add(s)

    db.session.commit()
    logger.info("Loading segments complete")

def list_segments():
    count = Segment.query.count()
    logging.info(f"Number of segments tracked: {count}")
    logging.info("Segment Id\t|\tSegment Name")
    for segment in Segment.query.all():
        logging.info(f"{segment.id}\t|\t{segment.name}")

def latest_entry():
    latest = SegmentEffort.query.order_by(SegmentEffort.date.desc()).first()
    if latest:
        logger.info(f"Latest recorded entry is from {latest.date}")
    else:
        logger.info("There are no entries stored")
