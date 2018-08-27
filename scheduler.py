import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from jobs import store_count_for_timeframe

logger = logging.getLogger(__name__)

sched = BlockingScheduler()


@sched.scheduled_job('cron', minute=0)
def day_job():
    logger.info("Storing today's counts")
    store_count_for_timeframe('today')


@sched.scheduled_job('cron', hour=23, minute=50)
def month_job():
    logger.info("Storing month's counts")
    store_count_for_timeframe('month')


sched.start()
