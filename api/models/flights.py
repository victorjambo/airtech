from .config.database import db
from .config.auditable_model import AuditableBaseModel

class Flight(AuditableBaseModel):
    """Class Flight model"""
    __tablename__ = 'flights'

    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Flight {self.name}>'
