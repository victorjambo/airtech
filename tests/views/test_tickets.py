"""Module of tests for tickets endpoints"""
import datetime
from os import getenv

from flask import json

from tests.mock.tickets import ticket_data
from api.utilities.constants import CHARSET
from api.utilities.messages import SUCCESS_MSG, ERROR_MSG

BASE_URL = getenv('API_BASE_URL_V1', default="/api/v1")


class TestTicketResource:
  """Test TicketResource POST endpoint
  """

  def test_list_tickets_succeeds(self, client, init_db, auth_header_token, new_flight):
    """Test successfully get Ticket
    """
    flight = new_flight.save()

    response = client.get(f'{BASE_URL}/flights/{flight.id}/tickets', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert isinstance(response_json["data"], list)
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Tickets")

  def test_single_tickets_succeeds(self, client, init_db, auth_header_token, new_ticket):
    """Test successfully get tickets
    """

    ticket = new_ticket.save()

    response = client.get(f'{BASE_URL}/tickets/{ticket.id}', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Ticket")

  def test_single_ticket_with_a_404_id_fails(self, client, init_db, auth_header_token):
    """Test fails get ticket
    """

    response = client.get(f'{BASE_URL}/tickets/-Lk04K16BglYRfMDyIRB', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 404
    assert response_json["status"] == "error"
    assert response_json["message"] == ERROR_MSG["not_found"].format("Ticket")

  def test_single_ticket_with_invalid_id_fails(self, client, init_db, auth_header_token):
    """Test fails get tickets
    """

    response = client.get(f'{BASE_URL}/tickets/)96', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["message"] == ERROR_MSG["invalid_id"]

  def test_create_ticket_with_valid_data_succeeds(self, client, init_db, auth_header_token, new_flight):
    """Test successfully ticket
    """
    flight = new_flight.save()

    data = json.dumps(ticket_data[-1])
    response = client.post(f'{BASE_URL}/flights/{flight.id}/tickets', headers=auth_header_token, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 201
    assert response_json["status"] == "success"
    assert response_json["message"] == SUCCESS_MSG["created"].format("Ticket")

  def test_list_tickets_succeeds(self, client, init_db, auth_header_token, new_flight):
    """Test successfully get Ticket
    """
    flight = new_flight.save()

    response = client.get(f'{BASE_URL}/flights/{flight.id}/tickets?seatNumber=512C&travelDate=2019-06-24', headers=auth_header_token)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert isinstance(response_json["data"], list)
    assert response_json["message"] == SUCCESS_MSG["fetched"].format("Tickets")

  def test_create_ticket_with_invalid_date_fails(self, client, init_db, auth_header_token, new_flight):
    """Test fails ticket
    """
    flight = new_flight.save()

    data = json.dumps({
      "seatNumber": "512E",
      "destination": "New York",
      "travelDate": "invalid"
    })
    response = client.post(f'{BASE_URL}/flights/{flight.id}/tickets', headers=auth_header_token, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["travelDate"][0] == ERROR_MSG["invalid_date"]

  def test_create_ticket_with_past_date_fails(self, client, init_db, auth_header_token, new_flight):
    """Test fails ticket
    """
    flight = new_flight.save()

    data = json.dumps({
      "seatNumber": "512E",
      "destination": "New York",
      "travelDate": "1990-01-01"
    })
    response = client.post(f'{BASE_URL}/flights/{flight.id}/tickets', headers=auth_header_token, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["travelDate"][0] == ERROR_MSG["past_date"]
