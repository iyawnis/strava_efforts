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
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.cli.command()
def load_segments():
    logger.info('Load segments')


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

