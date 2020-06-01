from app import db
from datetime import datetime
import csv
from models import Segment, SegmentEffort
def run_load():
    with open("last_export.csv", "r") as f:
        reader = csv.reader(f)
        columns = next(reader)
        for row in reader:
            last_effort = None
            segment_id = int(row[0])
            segment = Segment.query.get(segment_id)
            for date_index in range(1, len(columns)):
                effort = int(row[date_index])
                date_obj = datetime.strptime(columns[date_index], "%Y%m%d")
                s = SegmentEffort(effort_count=effort, athlete_count=0, date=date_obj,segment=segment)
                db.session.add(s)

        db.session.commit()

if __name__ == "__main__":
    run_load()
