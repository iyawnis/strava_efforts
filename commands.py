from flask import Blueprint
cmd = Blueprint('cmd', __name__)

@cmd.cli.command()
def load_models():
    print("Create all models")
    from app import db
    db.create_all()


@cmd.cli.command()
def update_segments():
    print('Load segments')
    from actions import load_segments
    load_segments()


@cmd.cli.command("collect_day")
def collect_day():
    print('Collecting day counts')
    from actions import store_segments_counts
    store_segments_counts()
