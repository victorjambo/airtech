from sqlalchemy.dialects.postgresql import JSON

from .config.database import db
from .config.auditable_model import AuditableBaseModel


class User(AuditableBaseModel):
    """Class User model"""
    __tablename__ = 'users'

    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    image = db.Column(JSON, nullable=True)

    tickets = db.relationship(
        'Ticket',
        backref='tickets',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def __repr__(self):
        return f'<User {self.username}>'
