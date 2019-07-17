"""Module for application factory."""
# System libraries
from os import getenv

# Third-party libraries
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restplus import Api
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Middlewares
from api import api_blueprint
from api.middlewares.base_validator import middleware_blueprint, ValidationError
from config import config, Config
from api.models.config.database import db

config_name = getenv('FLASK_ENV', default='production')
api = Api(api_blueprint, doc=False)

def initialize_errorhandlers(application):
    ''' Initialize error handlers '''
    application.register_blueprint(middleware_blueprint)
    application.register_blueprint(api_blueprint)


def create_app(config=config[config_name]):
    """Return app object given config object."""
    app = Flask(__name__)
    CORS(app)
    admin = Admin(app)
    app.config.from_object(config)

    # initialize error handlers
    initialize_errorhandlers(app)

    # bind app to db
    db.init_app(app)

    # import all models
    from api.models import User

    admin.add_view(ModelView(User, db.session))

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
