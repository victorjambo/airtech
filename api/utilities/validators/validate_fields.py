"""validate empty fields"""
import re
from marshmallow import ValidationError

from api.utilities.messages import ERROR_MSG

def validator_field(odj):
  """validator field
  """

  if not odj.strip():
    raise ValidationError(ERROR_MSG["required"])
