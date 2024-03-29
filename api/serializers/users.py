from marshmallow import (fields, post_load)

from api.models import User
from api.serializers.config.base_schemas import AuditableBaseSchema
from api.utilities.helpers.schemas import default_args
from api.utilities.validators.password_validator import password_validator
from api.utilities.validators.validate_duplicate import validate_duplicate
from api.utilities.validators.validate_fields import validator_field


class UserSchema(AuditableBaseSchema):
    """User model schema."""
    username = fields.String(**default_args(validate=validator_field))
    email = fields.Email(**default_args(validate=validator_field))
    password = fields.String(**default_args(validate=validator_field))
    image = fields.Dict()


class UserSignupSchema(UserSchema):
    """Auth signup Schema
    """
    password = fields.String(**default_args(validate=password_validator))

    @post_load
    def validate_duplicate_email(self, data):
        """Validate if email is taken
        """

        email = data.get("email")

        if email:
            data["email"] = data["email"].lower()
            validate_duplicate(User, User.email, email)

    @post_load
    def validate_duplicate_username(self, data):
        """Validate if username is taken
        """

        username = data.get("username")

        if username:
            data["username"] = data["username"].lower()
            validate_duplicate(User, User.username, username)
