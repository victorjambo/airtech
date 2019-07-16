from .base_model import BaseModel
from .database import db


class AuditableBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
