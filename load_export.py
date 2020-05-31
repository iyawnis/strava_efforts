from app import db
from datetime import datetime
import csv
from models import Segment, SegmentEffort
def run_load():
    with open("backup.csv", "r") as f:
        reader = csv.reader(f)
        columns = next(reader)
        for row in reader:
            last_effort = None
            segment_id = int(row[0])
            segment = Segment.query.get(segment_id)
            for date_index in range(len(columns) - 8 , 1 , -1):
                if last_effort is None:
                    last_effort = int(row[date_index + 1])
                effort = row[date_index]
                if effort == "":
                    print(f"missing effort for {columns[date_index]} and segment {segment_id}")
                    continue
                effort = int(effort)

                effort = last_effort - effort
                if effort:
                    last_effort = effort
                date_obj = datetime.strptime(columns[date_index], "%Y%m%d")
                s = SegmentEffort(effort_count=effort, athlete_count=0, date=date_obj,segment=segment)
                db.session.add(s)
            for date_index in range(len(columns) - 7, len(columns)):
                date_obj = datetime.strptime(columns[date_index], "%Y%m%d")
                effort = int(row[date_index])
                s = SegmentEffort(effort_count=effort, athlete_count=0, date=date_obj,segment=segment)
                db.session.add(s)

        db.session.commit()
