"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from datetime import datetime
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
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        segment_ids = [int(segment_id) for segment_id in form.segment_ids.data.split(',')]
        efforts = get_segments_effort_count(segment_ids, start_date, end_date)
        flash('Selected segment_ids="%s", start_date=%s, end_date=%s' %
              (segment_ids, start_date, end_date))
        flash('Result efforts: %s' % efforts)
        return redirect('/')
    return render_template('index.html',
                           title='Get Counters',
                           form=form)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


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
