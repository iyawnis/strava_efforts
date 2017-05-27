from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import date, timedelta
from wtforms.fields.html5 import DateField

dt = date.today()
start = dt - timedelta(days=dt.weekday())
end = start + timedelta(days=6)

class IndexForm(FlaskForm):
    segment_ids = StringField('segments', validators=[DataRequired()])
    start_date = DateField('start_date', default=start)
    end_date = DateField('end_date', default=end)
