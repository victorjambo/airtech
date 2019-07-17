"""Module for tickets resource"""

from main import api

from flask_restplus import Resource
from flask import request

from api.models import Ticket, Flight
from api.serializers.tickets import TicketSchema
from api.utilities.messages import SUCCESS_MSG
from api.utilities.validators.validate_id import validate_id
from api.middlewares.token_required import token_required


@api.route("/flights/<string:flight_id>/tickets")
class TicketResource(Resource):
  @token_required
  @validate_id
  def get(self, flight_id):
    """Tickets endpoint
    """
    Flight.get_or_404(flight_id)

    tickets = Ticket.query_()

    ticket_schema = TicketSchema(many=True)

    return {
      "status": "success",
      "message": SUCCESS_MSG["fetched"].format("Tickets"),
      "data": ticket_schema.dump(tickets).data
    }, 200

  @token_required
  @validate_id
  def post(self, flight_id):
    """Tickets endpoint
    """
    flight = Flight.get_or_404(flight_id)

    request_data = request.get_json()

    ticket_schema = TicketSchema()
    ticket_data = ticket_schema.load_object_into_schema(request_data)

    ticket_data["user_id"] = request.decoded_token["data"]["id"]
    ticket_data["flight_id"] = flight.id

    ticket = Ticket(**ticket_data)
    ticket.save()

    return {
      "status": "success",
      "message": SUCCESS_MSG["created"].format("Ticket"),
      "data": ticket_schema.dump(ticket).data
    }, 201


@api.route("/tickets/<string:ticket_id>")
class SingleTicketResource(Resource):
  @token_required
  @validate_id
  def get(self, ticket_id):
    """single Ticket endpoint
    """

    ticket = Ticket.get_or_404(ticket_id)

    ticket_schema = TicketSchema()

    return {
      "status": "success",
      "message": SUCCESS_MSG["fetched"].format("Ticket"),
      "data": ticket_schema.dump(ticket).data
    }, 200
