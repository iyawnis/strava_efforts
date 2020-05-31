from app import db

class Segment(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String)
    efforts = db.relationship('SegmentEffort', backref='segment', lazy=True)
    created_at = db.Column(db.Date)


class SegmentEffort(db.Model):
    __table_args__ = (
        db.UniqueConstraint('segment_id', 'date'),)

    id = db.Column(db.Integer, primary_key=True)
    effort_count = db.Column(db.Integer)
    segment_id = db.Column(db.Integer, db.ForeignKey("segment.id"), nullable=False)
    athlete_count = db.Column(db.Integer)
    date = db.Column(db.Date, index=True)
