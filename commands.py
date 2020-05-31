import logging
from datetime import date
from flask import Blueprint

logger = logging.getLogger(__name__)
cmd = Blueprint('cmd', __name__)

@cmd.cli.command("load_models")
def load_models():
    logger.info("Create all models")
    from app import db
    db.create_all()


@cmd.cli.command("update_segments")
def update_segments():
    logger.info('Load segments')
    from actions import load_segments
    load_segments()


@cmd.cli.command("collect_today")
def collect_day():
    logger.info('Collecting day counts')
    from actions import store_segments_counts
    store_segments_counts()


@cmd.cli.command("count_today")
def count_today():
    from models import SegmentEffort
    today = date.today()
    count = SegmentEffort.query.filter_by(date=today).count()
    logger.info(f'{count} efforts collected for today')

@cmd.cli.command("delete_today")
def delete_today():
    from models import SegmentEffort
    from app import db
    today = date.today()
    count = SegmentEffort.query.filter_by(date=today).delete()
    db.session.commit()

    logger.info(f'{count} efforts deleted for today')
