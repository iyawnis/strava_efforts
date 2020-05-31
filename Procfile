web: gunicorn -w 4 -b "0.0.0.0:$PORT" app:app
scheduler: python scheduler.py
release: bash startup.sh
