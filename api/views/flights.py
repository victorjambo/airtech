"""Module for flights resource"""
import os
from main import api

from flask_restplus import Resource

from main import cache
from api.models import Flight
from api.serializers.flights import FlightSchema
from api.utilities.messages import SUCCESS_MSG
from api.utilities.validators.validate_id import validate_id
from api.middlewares.token_required import token_required

FLASK_ENV = os.getenv('FLASK_ENV', default='development')


@api.route("/flights")
class FlightResource(Resource):
  @token_required
  @cache.cached(timeout=50, key_prefix='flights')
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
  @token_required
  @validate_id
  def get(self, flight_id):
    """single flight endpoint
    """
    mapper = {
      'testing': self.get_flight_testing,
      'development': self.get_flight,
      'production': self.get_flight
    }

    flight = Flight.get_or_404(flight_id)

    flight_schema = FlightSchema(only=['id', 'name'])

    return {
      "status": "success",
      "message": SUCCESS_MSG["fetched"].format("Flight"),
      "data": flight_schema.dump(flight).data
    }, 200

  @cache.cached(timeout=50, key_prefix='single_flight')
  def get_flight(self, flight_id):
    return Flight.get_or_404(flight_id)

  def get_flight_testing(self, flight_id):
    return Flight.get_or_404(flight_id)
