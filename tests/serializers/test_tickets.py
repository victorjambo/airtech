"""Module for testing Ticket schema"""
import pytest

from api.serializers.tickets import TicketSchema
from tests.mock.tickets import ticket_data


class TestTicketSchema:
  """Test Ticket schema
  """

  def test_ticket_schema_with_valid_data_succeeds(self, init_db):
    """Should pass when valid data is supplied
    """
    flight_schema = TicketSchema()
    data = flight_schema.load_object_into_schema(ticket_data[-1])

    assert data["seat_number"] == ticket_data[-1]["seat_number"]
