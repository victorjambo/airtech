"""Module for flights resource"""

from main import api

from flask_restplus import Resource

from api.models import Flight
from api.serializers.flights import FlightSchema
from api.utilities.messages import SUCCESS_MSG
from api.utilities.validators.validate_id import validate_id


@api.route("/flights")
class FlightResource(Resource):
  def get(self):
    """flights endpoint
    """

    flights = Flight.query_()

    flight_schema = FlightSchema(many=True, only=['id', 'name'])

    return {
      "status": "success",
      "message": SUCCESS_MSG["fetched"].format("Flights"),
      "data": flight_schema.dump(flights).data
    }, 200


@api.route("/flights/<string:flight_id>")
class SingleFlightResource(Resource):
  @validate_id
  def get(self, flight_id):
    """single flight endpoint
    """

    flight = Flight.get_or_404(flight_id)

    flight_schema = FlightSchema(only=['id', 'name'])

    return {
      "status": "success",
      "message": SUCCESS_MSG["fetched"].format("Flight"),
      "data": flight_schema.dump(flight).data
    }, 200
