from sqlalchemy.orm import column_property
from sqlalchemy import select, func

from .config.database import db
from .config.auditable_model import AuditableBaseModel
from api.models.tickets import Ticket

class Flight(AuditableBaseModel):
    """Class Flight model"""
    __tablename__ = 'flights'

    name = db.Column(db.String(), nullable=False)
    tickets = db.relationship(
        'Ticket',
        backref='bookings',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def __repr__(self):
        return f'<Flight {self.name}>'
