"""Module for application factory."""
# System libraries
import redis
from os import getenv

# Third-party libraries
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restplus import Api
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from celery import Celery
from flask_caching import Cache
from flask_apscheduler import APScheduler

# Middlewares
from api import api_blueprint
from api.middlewares.base_validator import middleware_blueprint, ValidationError
from config import config, Config
from api.models.config.database import db

config_name = getenv('FLASK_ENV', default='production')
api = Api(api_blueprint, doc=False)
mail = Mail()
cache = Cache()
scheduler = APScheduler()


def cache_type():
    """Check if redis is running. used for caching endpoints
    """
    rs = redis.Redis("localhost")
    try:
        rs.ping()
        if config_name != 'testing':
            return 'redis'
    except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
        return 'simple'
    return 'simple'

config[config_name].CACHE_TYPE = cache_type()

# Celery object and configures it with the broker (redis).
# __name__ is the app.name, which will be initialized later
TASK_LIST = ['celery_src.tasks', 'api.middlewares.send_mail']
celery_app = Celery(
    __name__, broker=Config.CELERY_BROKER_URL, include=TASK_LIST)

def initialize_errorhandlers(application):
    ''' Initialize error handlers '''
    application.register_blueprint(middleware_blueprint)
    application.register_blueprint(api_blueprint)


def create_app(config=config[config_name]):
    """Return app object given config object."""
    app = Flask(__name__)
    app.secret_key = getenv('SECRET', default='secret-key')
    CORS(app)
    admin = Admin(app)
    app.config.from_object(config)
    celery_app.conf.update(app.config)

    mail.init_app(app)
    cache.init_app(app)

    # BG tasks
    scheduler.init_app(app)
    scheduler.start()

    # initialize error handlers
    initialize_errorhandlers(app)

    # bind app to db
    db.init_app(app)
    db.app = app

    # import all models
    from api.models import User, Flight, Ticket

    admin.add_view(ModelView(Flight, db.session))

    # import views
    import api.views


    # initialize migration scripts
    migrate = Migrate(app, db)

    return app


@api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised"""

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
