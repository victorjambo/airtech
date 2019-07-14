from os import getenv
from flask import jsonify

from main import create_app
from config import config

from api.models.config.database import db


config_name = getenv('FLASK_ENV', default='development')
app = create_app(config[config_name])


@app.route('/')
def index():
    return jsonify(dict(message='Welcome to the Stack Overflow API'))

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
