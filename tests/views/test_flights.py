"""Module of tests for flights endpoints"""
from os import getenv

from flask import json

from api.models import User
from tests.mock.users import user_data
from api.utilities.constants import CHARSET
from api.utilities.messages import SUCCESS_MSG, ERROR_MSG

BASE_URL = getenv('API_BASE_URL_V1', default="/api/v1")


class TestFlightResource:
  """Test FlightResource POST endpoint
  """

  def test_list_flights_succeeds(self, client, init_db, auth_header):
    """Test successfully get flights
    """

    response = client.get(f'{BASE_URL}/flights', headers=auth_header)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert isinstance(response_json["data"], list)
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Flights")

  def test_single_flight_succeeds(self, client, init_db, auth_header, new_flight):
    """Test successfully get flights
    """

    flight = new_flight.save()

    response = client.get(f'{BASE_URL}/flights/{flight.id}', headers=auth_header)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Flight")
