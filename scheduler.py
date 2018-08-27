from apscheduler.schedulers.blocking import BlockingScheduler
from jobs import store_count_for_timeframe

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def day_job():
    store_count_for_timeframe('today')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
