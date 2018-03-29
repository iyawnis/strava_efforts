"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from datetime import datetime
from functools import reduce
from flask import Flask, render_template, flash, request, redirect, url_for
from forms import IndexForm
from strava import get_segments_effort_count

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Routing for your application.
###

@app.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    results = {}
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        segment_ids = [int(segment_id) for segment_id in form.segment_ids.data.split(',')]
        efforts = get_segments_effort_count(segment_ids, start_date, end_date)
        results = {
            'segment_ids': segment_ids,
            'start_date': start_date,
            'end_date': end_date,
            'efforts': efforts,
            'total_efforts': reduce(lambda x, y: x + y, efforts.values())
        }
    return render_template(
        'index.html',
        form=form,
        results=results
    )


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
    app.run(debug=True)
