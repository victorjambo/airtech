""" Module for base marshmallow schema. """
from marshmallow import Schema, fields

from api.middlewares.base_validator import ValidationError


class BaseSchema(Schema):
    """Base marshmallow schema with common attributes."""
    id = fields.String(dump_only=True)
    deleted = fields.Boolean(dump_only=True)

    def load_json_into_schema(self, data):
        """Helper function to load raw json request data into schema"""
        data, errors = self.loads(data)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data

    def load_object_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema"""
        data, errors = self.load(data, partial=partial)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data


class AuditableBaseSchema(BaseSchema):
    """ Base marshmallow schema for auditable models. """
    created_at = fields.DateTime(dump_only=True, dump_to='createdAt')
    updated_at = fields.DateTime(dump_only=True, dump_to='updatedAt')
    deleted_at = fields.DateTime(dump_only=True, dump_to='deletedAt')
    created_by = fields.String(dump_only=True, dump_to='createdBy')
    updated_by = fields.String(dump_only=True, dump_to='updatedBy')
    deleted_by = fields.String(dump_only=True, dump_to='deletedBy')
