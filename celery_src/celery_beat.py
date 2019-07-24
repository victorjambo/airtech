from celery.schedules import crontab
from celery import Celery

from config import Config

celery_scheduler = Celery(__name__, broker=Config.CELERY_BROKER_URL)

celery_scheduler.conf.enable_utc = False

celery_scheduler.conf.beat_schedule = {
    'run-flight-check-every-day': {
        'task': 'send_emails',
        'schedule': crontab(hour="*/24")
    },
}
