from app import db
from datetime import datetime, date
import csv
from models import Segment, SegmentEffort
def run_load():
    with open("edited_data.csv", "r") as f:
        reader = csv.reader(f)
        columns = next(reader)
        first = date(2020,5,30)
        SegmentEffort.query.filter(SegmentEffort.date < first).delete()
        for row in reader:
            last_effort = None
            segment_id = int(row[0])
            segment = Segment.query.get(segment_id)
            for date_index in range(len(columns) - 1, 1 , -1):

                if last_effort is None:
                    last_effort = SegmentEffort.query.filter_by(segment=segment, date=first).first().effort_count
                effort = row[date_index]
                if effort == "":
                    continue
                effort = int(effort)

                effort = last_effort - effort
                if effort:
                    last_effort = effort
                date_obj = datetime.strptime(columns[date_index], "%Y%m%d")
                s = SegmentEffort(effort_count=effort, athlete_count=0, date=date_obj,segment=segment)
                db.session.add(s)

        db.session.commit()

if __name__ == "__main__":
    run_load()
