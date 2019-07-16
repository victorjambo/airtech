import os
import pytest

from flask import current_app, request

from config import config
from main import create_app
from api.models import User
from api.models.config.database import db
from tests.mock.users import user_data
from api.utilities.constants import MIMETYPE, MIMETYPE_TEXT


config_name = 'testing'
os.environ['FLASK_ENV'] = config_name
BASE_URL = os.getenv('API_BASE_URL_V1')

@pytest.yield_fixture(scope='session')
def app():
  """Setup our flask test app, this only gets executed once.
  """
  _app = create_app(config[config_name])

  # Establish an application context before running the tests.
  ctx = _app.app_context()
  ctx.push()

  yield _app

  ctx.pop()


@pytest.fixture(scope='function')
def client(app):
  """Setup an app client, this gets executed for each test function.
  """
  yield app.test_client()

@pytest.fixture(scope='module')
def request_ctx():
  """Setup a request client, this gets executed for each test module.
  """
  ctx = current_app.test_request_context()
  ctx.push()
  yield ctx
  ctx.pop()

@pytest.fixture(scope='module')
def init_db(app):
  """initialize db
  """
  db.create_all()
  yield db
  db.session.close()
  db.drop_all()

@pytest.fixture(scope='module')
def auth_header():
  """auth header
  """
  return {
    'Content-Type': MIMETYPE,
    'Accept': MIMETYPE
  }

@pytest.fixture(scope="module")
def new_user(app):
  """new user
  """
  return User(**user_data["victor"])
