import re

from .database import db
from api.middlewares.base_validator import ValidationError
from api.utilities.messages import ERROR_MSG
from api.utilities.filters import Filters


class ModelOperations(object):
    def save(self):
        """Save a model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update_(self, **kwargs):
        """update entries
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        db.session.commit()

    def delete(self):
        """Delete a model instance
        """
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def query_(cls, filter_condition=None):
        """Dynamic filter
        """
        if filter_condition:
            filter = Filters(cls)
            return filter.filter_query(filter_condition)

        return cls.query.filter_by()

    @classmethod
    def get_username_or_404(cls, username):
        """Get user by username or return 404
        """
        record = cls.query.filter_by(username=username).first()

        if not record:
            raise ValidationError({"message": ERROR_MSG["not_found"].format("User")}, 404)

        return record

    @classmethod
    def get(cls, id):
        """Return entries by id
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def count(cls):
        """Returns total entries in the database
        """
        counts = cls.query.count()
        return counts

    @classmethod
    def get_or_404(cls, id):
        """Return entries by id
        """

        record = cls.query.get(id)

        if not record:
            raise ValidationError(
                {
                    'message':
                    f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'
                },
                404)

        return record
