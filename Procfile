web: gunicorn app:app --workers 4 --log-level info --log-file -
worker: celery -A celery_init.celery_app worker -l info
beat: celery -A celery_src.celery_beat beat -l info
release: flask db upgrade
