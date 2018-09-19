import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from jobs import store_count_for_timeframe

logger = logging.getLogger(__name__)

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=21)
def day_job():
    logger.info("Storing today's counts")
    store_count_for_timeframe('today')


@sched.scheduled_job('cron', day_of_week=6, hour=21, minute=5)
def week_job():
    logger.info("Storing week's counts")
    store_count_for_timeframe('week')


@sched.scheduled_job('cron', hour=21)
def month_job():
    logger.info("Storing month's counts")
    store_count_for_timeframe('month')


sched.start()
