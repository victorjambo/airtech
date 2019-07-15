"""validate password against regex"""
import re
from marshmallow import ValidationError

from api.utilities.messages import ERROR_MSG

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", re.I | re.UNICODE)

def password_validator(password):
  """password_validator
  """

  if not PASSWORD_REGEX.match(password):
    raise ValidationError(ERROR_MSG["password"])
