"""Module for testing Flight schema"""
import pytest

from api.serializers.flights import FlightSchema
from tests.mock.flights import flight_data


class TestFlightSchema:
  """Test Flight schema
  """

  def test_flight_schema_with_valid_data_succeeds(self, init_db):
    """Should pass when valid permission type is supplied
    """
    flight_schema = FlightSchema()
    data = flight_schema.load_object_into_schema(flight_data[-1])

    assert data["name"] == flight_data[-1]["name"]
