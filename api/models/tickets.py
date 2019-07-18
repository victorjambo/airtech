from .config.database import db
from .config.auditable_model import AuditableBaseModel

class Ticket(AuditableBaseModel):
  """Class Ticket model"""
  __tablename__ = 'tickets'

  seat_number = db.Column(db.String(), nullable=False)
  destination = db.Column(db.String(), nullable=False)
  travel_date = db.Column(db.String(), nullable=False)

  user_id = db.Column(db.String, db.ForeignKey('users.id'))
  flight_id = db.Column(db.String, db.ForeignKey('flights.id'))

  user = db.relationship('User', lazy='joined')
  flight = db.relationship('Flight', lazy='joined')


  def __repr__(self):
    return f'<Ticket {self.seat_number}>'
