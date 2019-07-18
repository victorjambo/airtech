from celery_src.celery_beat import celery_scheduler

@celery_scheduler.task(name='check_flight_dates')
def check_flight_dates():
  pass
