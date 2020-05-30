import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger(__name__)

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=23)
def day_job():
    logger.info("Storing today's counts")
    from actions import store_segments_counts
    store_segments_counts()

sched.start()
