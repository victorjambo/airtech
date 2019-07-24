"""Celery Tasks"""

from main import celery_app

from api.middlewares.send_mail import periodic_email

@celery_app.task(name="sample_scheduler")
def sample_scheduler():
    """Sample to test `/celery` endpoint has scheduled tasks
    """

    return dict(message="sample scheduler")

@celery_app.task(name='send_emails')
def send_email_task():
  """Call send email task
  """

  periodic_email()
  return dict(message="Emails sent")
