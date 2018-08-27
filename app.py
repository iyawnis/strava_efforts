"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import io
import csv
import os
from collections import OrderedDict
from datetime import datetime
from functools import reduce
from flask import make_response, Flask, render_template, flash, request, redirect, url_for
from forms import IndexForm
from store import get_data_for_timeframe


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


###
# Routing for your application.
###

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html' )


@app.route('/export/month/', methods=['GET'])
def export_month():
    return export_for_timeframe('month')


@app.route('/export/today/', methods=['GET'])
def export_today():
    return export_for_timeframe('today')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


def export_for_timeframe(timeframe):
    data = get_data_for_timeframe(timeframe)
    segment_dates = [list(dates.keys()) for dates in data.values()]
    unique_dates = {date for all_dates in segment_dates for date in all_dates}
    unique_dates = sorted(unique_dates)
    for segment, segment_dates in data.items():
        for unique_date in unique_dates:
            if unique_date not in segment_dates:
                segment_dates[unique_date] = 0

    si = io.StringIO()
    cw = csv.writer(si)
    columns = ['segment-id'] + list(unique_dates)
    cw.writerow(columns)
    for segment, segment_dates in data.items():
        segment_dates = OrderedDict(segment_dates.items())
        row = [segment] + list(segment_dates.values())
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

