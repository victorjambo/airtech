from api.middlewares.send_mail import periodic_email


def scheduler():
  """scheduler to send periodic emails
  """

  periodic_email()
