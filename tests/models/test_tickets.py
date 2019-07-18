"""Test Ticket Model Module"""

from api.models import Ticket


class TestTicketModelClass:
  """Test TicketModel
  """
  def test_new_ticket(self, init_db, new_ticket):
    """Test create new Ticket
    """
    ticket = new_ticket
    assert ticket == new_ticket.save()

  def test_count(self):
    """Test model data count
    """
    assert Ticket.count() == 1

  def test_query(self):
    """Test querying Ticket works
    """
    ticket_query = Ticket.query_()
    assert ticket_query.count() == 1
    assert isinstance(ticket_query.all(), list)

  def test_update(self, new_ticket):
    """test update Ticket model
    """
    new_ticket.update_(seat_number='Modified')
    assert new_ticket.seat_number == 'Modified'

  def test_delete(self, new_ticket):
    """test delete Ticket model
    """
    new_ticket.delete()
    assert Ticket.get(new_ticket.id) is None

  def test_ticket_model_string_representation(self, new_ticket):
    """Should compute the string representation of a Ticket
    """
    assert repr(new_ticket) == f'<Ticket {new_ticket.seat_number}>'
