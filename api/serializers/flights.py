"""flight schema module"""

from marshmallow import fields

from api.serializers.config.base_schemas import AuditableBaseSchema
from api.utilities.helpers.schemas import default_args


class FlightSchema(AuditableBaseSchema):
    """Flight model schema."""
    name = fields.String(**default_args())
