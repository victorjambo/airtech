from os import getenv
from flask import jsonify

from main import create_app, celery_app
from config import config
from celery_src.state import celery_task_state
from api.models.config.database import db


config_name = getenv('FLASK_ENV', default='development')
app = create_app(config[config_name])


@app.route('/')
def index():
    return jsonify(dict(message='Welcome to the Stack Overflow API'))

@app.route('/celery/health')
def celery_stats():
    """Checks tasks queued by celery.
    """

    msg = None

    ins = celery_app.control.inspect()

    try:
        tasks = ins.registered_tasks()
        msg = {"tasks": tasks, "status": "Celery up"}
    except ConnectionError:
        msg = {"status": "Redis server down"}
    except Exception:
        msg = {"status": "Celery down"}

    return jsonify(dict(message=msg)), 200

@app.route('/celery-beat/health')
def celery_beat_stats():
    """Checks tasks scheduled by celery-beat
    """
    import shelve

    down_tasks = {}
    ok_tasks = {}

    file_data = shelve.open(
        'celerybeat-schedule'
    )  # Name of the file used by PersistentScheduler to store the last run times of periodic tasks.

    entries = file_data.get('entries')

    if not entries:
        return jsonify(dict(error="celery-beat service not available")), 503

    for task_name, task in entries.items():

        try:
            celery_task_state(
                task, task_name, ok_tasks, down_tasks, is_cron_task=False)

        except AttributeError:

            celery_task_state(task, task_name, ok_tasks, down_tasks)

    if down_tasks:
        return jsonify(dict(message={
            'Down tasks': down_tasks,
        })), 503

    return jsonify(dict(message={'Okay tasks': ok_tasks})), 200

@app.cli.command()
def migrate():
    """Create tables
    """

    db.migrations()

@app.cli.command()
def drop():
    """Drop tables
    """

    db.drop_tables()

if __name__ == '__main__':
    app.run()
