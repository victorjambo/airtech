import re

from .database import db
from api.middlewares.base_validator import ValidationError


class ModelOperations(object):
    def save(self):
        """Save a model instance"""
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, kwargs):
        """ update entries """
        for field, value in kwargs.items():
            setattr(self, field, value)
        return self

    def delete(self):
        """Delete a model instance"""
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def query_(cls, data):
        return cls.query.filter_by(username=data['username']).first()

    @classmethod
    def get_or_404(cls, id):
        """
        return entries by id
        """

        record = cls.query.get(id)

        if not record:
            raise ValidationError(
                {
                    'message':
                    f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'  # noqa
                },
                404)

        return record
