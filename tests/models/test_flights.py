"""Test Flight Model Module"""

from api.models import Flight


class TestFlightModelClass:
  """Test FlightModel
  """
  def test_new_flight(self, init_db, new_flight):
    """Test create new Flight
    """
    flight = new_flight
    assert flight == new_flight.save()

  def test_count(self):
    """Test model data count
    """
    assert Flight.count() == 1

  def test_query(self):
    """Test querying Flight works
    """
    flight_query = Flight.query_()
    assert flight_query.count() == 1
    assert isinstance(flight_query.all(), list)

  def test_update(self, new_flight):
    """test update Flight model
    """
    new_flight.update_(name='Modified')
    assert new_flight.name == 'Modified'

  def test_delete(self, new_flight):
    """test delete Flight model
    """
    new_flight.delete()
    assert Flight.get(new_flight.id) is None

  def test_flight_model_string_representation(self, new_flight):
    """Should compute the string representation of a Flight
    """
    assert repr(new_flight) == f'<Flight {new_flight.name}>'
