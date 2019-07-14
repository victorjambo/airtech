from marshmallow import (fields, post_load)

from api.serializers.config.base_schemas import AuditableBaseSchema


class UserSchema(AuditableBaseSchema):
    """User model schema."""
    name = fields.String()
    email = fields.String()
