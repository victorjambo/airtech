from os import getenv
from flask_mail import Message
from flask import jsonify, render_template
from main import mail

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
