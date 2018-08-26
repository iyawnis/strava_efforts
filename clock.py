from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from strava import get_efforts_for_segment
from store import set_segment_date_count


sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=1)
def timed_job():
    segment_id = '7550717'
    print('This job is run every three minutes.')
    effort_count = get_efforts_for_segment(seg_id)
    set_segment_date_count(seg_id, datetime.today(), effort_count())


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()

