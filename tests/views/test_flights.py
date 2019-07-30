"""Module of tests for flights endpoints"""
import datetime
from os import getenv

from flask import json

from api.models import User
from tests.mock.users import user_data
from tests.helpers.generate_token import generate_token
from api.utilities.constants import CHARSET
from api.utilities.messages import SUCCESS_MSG, ERROR_MSG, jwt_errors

BASE_URL = getenv('API_BASE_URL_V1', default="/api/v1")


class TestFlightResource:
  """Test FlightResource POST endpoint
  """

  def test_list_flights_succeeds(self, client, init_db, auth_header_token):
    """Test successfully get flights
    """

    response = client.get(f'{BASE_URL}/flights', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert isinstance(response_json["data"], list)
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Flights")

  def test_single_flight_succeeds(self, client, init_db, auth_header_token, new_flight):
    """Test successfully get flights
    """

    flight = new_flight.save()

    response = client.get(f'{BASE_URL}/flights/{flight.id}', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Flight")

  def test_single_flight_with_a_404_id_fails(self, client, init_db, auth_header_token):
    """Test fails get flights
    """

    response = client.get(f'{BASE_URL}/flights/-Lk04K16BglYRfMDyIRB', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 404
    assert response_json["status"] == "error"
    assert response_json["message"] == ERROR_MSG["not_found"].format("Flight")

  def test_single_flight_with_invalid_id_fails(self, client, init_db, auth_header_token):
    """Test fails get flights
    """

    response = client.get(f'{BASE_URL}/flights/)96', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["message"] == ERROR_MSG["invalid_id"]


class TestFlightJWTFailResource:
  """Test endpoints without token
  """
  def test_get_flights_NO_TOKEN_MSG_fails(self, client, init_db, auth_header):
    """Test fails get flights
    """

    response = client.get(f'{BASE_URL}/flights', headers=auth_header)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 401
    assert response_json["status"] == "error"
    assert response_json["message"] == jwt_errors['NO_TOKEN_MSG']

  def test_get_flights_NO_BEARER_MSG_fails(self, client, init_db, auth_header):
    """Test fails get flights
    """
    auth_header['Authorization'] = 'token'
    response = client.get(f'{BASE_URL}/flights', headers=auth_header)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 401
    assert response_json["status"] == "error"
    assert response_json["message"] == jwt_errors['NO_BEARER_MSG']

  def test_get_flights_INVALID_TOKEN_MSG_fails(self, client, init_db, auth_header):
    """Test fails get flights
    """
    auth_header['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImlkIjoiLUxqcjNOLTQ0cUFsTnhIc1RUU0wiLCJlbWFpbCI6Im11dGFpQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoidmljdG9yIn0sImV4cCI6MTU2MzM5NzQxNH0.d9aPi7nlxC1XLTWhE1AO2ixQfTAh0wt9-rswM8G6E0'
    response = client.get(f'{BASE_URL}/flights', headers=auth_header)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 401
    assert response_json["status"] == "error"
    assert response_json["message"] == jwt_errors['INVALID_TOKEN_MSG']

  def test_get_flights_EXPIRED_TOKEN_MSG_fails(self, client, init_db, auth_header):
    """Test fails get flights
    """
    expired_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    auth_header['Authorization'] = generate_token(expired_date)

    response = client.get(f'{BASE_URL}/flights', headers=auth_header)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 401
    assert response_json["status"] == "error"
    assert response_json["message"] == jwt_errors['EXPIRED_TOKEN_MSG']
