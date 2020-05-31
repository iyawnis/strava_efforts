"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import io
import os
import sys
from flask import make_response, Flask, render_template, redirect, request
from strava import requires_authorization, get_authorization_url, exchange_code_for_token
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
root.addHandler(handler)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import *
migrate = Migrate(app, db)


from commands import cmd
app.register_blueprint(cmd)


###
# Routing for your application.
###

@app.route('/', methods=['GET', 'POST'])
def index():
    authorization_url = None
    if requires_authorization():
        authorization_url = get_authorization_url()
    segment_count = Segment.query.count()
    latest_date = SegmentEffort.query.order_by(SegmentEffort.date.desc()).first().date

    return render_template('index.html', authorization_url=authorization_url, segment_count=segment_count, latest_date=latest_date)

@app.route('/authorization', methods=['GET'])
def auth():
    code = request.args.get('code')
    access_token = exchange_code_for_token(code)
    return redirect("/")



@app.route('/export', methods=['GET'])
def export_today():
    from actions import database_to_dataframe
    si = io.StringIO()
    df = database_to_dataframe()
    df.to_csv(si)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


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
