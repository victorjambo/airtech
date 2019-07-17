"""Ticket schema module"""

from marshmallow import fields

from api.serializers.config.base_schemas import AuditableBaseSchema
from api.utilities.helpers.schemas import default_args
from api.serializers.users import UserSchema
from api.serializers.flights import FlightSchema


class TicketSchema(AuditableBaseSchema):
  """Ticket model schema.
  """
  seat_number = fields.String(load_from="seatNumber", dump_to="seatNumber", **default_args())
  destination = fields.String(**default_args())
  travel_date = fields.String(load_from="travelDate", dump_to="travelDate", **default_args())

  user = fields.Nested(
    UserSchema,
    dump_only=True,
    only=['id', 'username', 'email'])

  flight = fields.Nested(
    FlightSchema,
    dump_only=True,
    only=['id', 'name'])
