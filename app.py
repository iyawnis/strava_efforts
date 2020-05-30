"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import io
import csv
import click
import logging
import os
from flask_restplus import Resource, Api
from collections import OrderedDict
from flask import make_response, Flask, render_template, redirect, request
from store import get_data
from jobs import store_segments_counts
from strava import requires_authorization, get_authorization_url, exchange_code_for_token

logger = logging.getLogger(__name__)
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.cli.command()
def collect_day():
    logger.info('Collecting day counts')
    store_segments_counts()

###
# Routing for your application.
###

@app.route('/', methods=['GET', 'POST'])
def index():
    authorization_url = None
    if requires_authorization():
        authorization_url = get_authorization_url()
    return render_template('index.html', authorization_url=authorization_url)

@app.route('/authorization', methods=['GET'])
def auth():
    code = request.args.get('code')
    access_token = exchange_code_for_token(code)
    return redirect("/")


@app.route('/export/month/', methods=['GET'])
def export_month():
    return export_for_timeframe('month')


@app.route('/export/today/', methods=['GET'])
def export_today():
    return export_for_timeframe('today')


@app.route('/export/year/', methods=['GET'])
def export_year():
    return export_for_timeframe('year')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

def clean_values(segment_counts):
    for v in segment_counts.values():
        if isinstance(v, int) or v is None:
            yield v
        else:
            yield v["effort"]

def data_for_timeframe(timeframe):
    data = get_data()
    segment_dates = [list(dates.keys()) for dates in data.values()]
    unique_dates = {date for all_dates in segment_dates for date in all_dates}
    unique_dates = sorted(unique_dates)
    for segment, segment_dates in data.items():
        for unique_date in unique_dates:
            if unique_date not in segment_dates:
                segment_dates[unique_date] = None

    rows = [['segment-id'] + list(unique_dates)]
    for segment, segment_dates in data.items():
        segment_dates = OrderedDict(sorted(segment_dates.items()))
        row = [segment] + list(clean_values(segment_dates))
        rows.append(row)
    return rows

def export_for_timeframe(timeframe):
    si = io.StringIO()
    cw = csv.writer(si)
    rows = data_for_timeframe(timeframe)
    cw.writerows(rows)
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
    debug = os.environ.get('DEBUG', False)
    app.run(debug=True, host="0.0.0.0", port=8888)

