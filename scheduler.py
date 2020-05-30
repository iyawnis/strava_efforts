import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from jobs import store_segments_counts

logger = logging.getLogger(__name__)

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=21)
def day_job():
    logger.info("Storing today's counts")
    store_segments_counts()

sched.start()
