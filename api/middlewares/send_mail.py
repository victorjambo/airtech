from os import getenv
from flask_mail import Message
from flask import jsonify, render_template
from main import mail
from datetime import datetime, timedelta

from api.models import Ticket

def send_email(ticket):
  """Send email
  """

  user = ticket.user
  sender = getenv('EMAIL_HOST_USER')
  path = getenv('BASE_PATH')

  msg = Message(
      'Travel Reminder',
      sender=sender,
      recipients=[user.email]
  )
  msg.html = render_template('email.html', ticket=ticket, path=path)

  mail.send(msg)

def periodic_email():
  """Send emails to flights in the next 24 hours
  """
  next_24 = datetime.utcnow() + timedelta(hours=24)
  tickets = Ticket.query.filter(Ticket.travel_date >= datetime.now(), Ticket.travel_date <= next_24).all()
  for ticket in tickets:
    send_email(ticket)
