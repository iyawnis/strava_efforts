import logging
from flask import Blueprint

logger = logging.getLogger(__name__)
cmd = Blueprint('cmd', __name__)

@cmd.cli.command()
def load_models():
    logger.info("Create all models")
    from app import db
    db.create_all()


@cmd.cli.command()
def update_segments():
    logger.info('Load segments')
    from actions import load_segments
    load_segments()


@cmd.cli.command("collect_day")
def collect_day():
    logger.info('Collecting day counts')
    from actions import store_segments_counts
    store_segments_counts()
