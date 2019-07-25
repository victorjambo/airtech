import os
import pytest

from flask import current_app, request

from config import config
from main import create_app
from api.models import User, Flight, Ticket
from api.models.config.database import db
from tests.mock.users import user_data
from tests.mock.flights import flight_data
from tests.mock.tickets import ticket_data
from api.utilities.constants import MIMETYPE, MIMETYPE_TEXT
from tests.helpers.generate_token import generate_token


config_name = 'testing'
os.environ['FLASK_ENV'] = config_name
os.environ['SECRET'] = "testing-secret-key"
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

@pytest.fixture(scope='module')
def auth_header_token():
  """auth header with token
  """
  return {
    'Content-Type': MIMETYPE,
    'Accept': MIMETYPE,
    'Authorization': generate_token()
  }

@pytest.fixture(scope="module")
def new_user(app):
  """new user
  """
  return User(**user_data["victor"])

@pytest.fixture(scope="module")
def new_flight(app):
  """new Flight
  """
  return Flight(**flight_data[0])

@pytest.fixture(scope="module")
def new_ticket(app):
  """new Ticket
  """
  return Ticket(**ticket_data[0])

@pytest.fixture(scope="module")
def cloudinary_mock_response():
  return {
    "public_id": "public-id",
    "url": "http://hello.com/here"
  }
