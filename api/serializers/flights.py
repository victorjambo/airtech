from marshmallow import (fields, post_load)

from api.models import User
from api.serializers.config.base_schemas import AuditableBaseSchema
from api.utilities.helpers.schemas import default_args
from api.utilities.validators.password_validator import password_validator
from api.utilities.validators.validate_duplicate import validate_duplicate


class FlightSchema(AuditableBaseSchema):
    """Flight model schema."""
    name = fields.String(**default_args())
