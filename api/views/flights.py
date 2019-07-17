"""Module for flights resource"""

from main import api

from flask_restplus import Resource

from api.models import Flight
from api.serializers.flights import FlightSchema
from api.utilities.messages import SUCCESS_MSG


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
