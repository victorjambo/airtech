"""Validate Duplicate from models"""
from marshmallow import ValidationError

from api.utilities.messages import ERROR_MSG

def validate_duplicate(model, *query):
  """Validate duplicate fields from models
  """
  field, value = query
  entry = model.query.filter(field == value).first()

  if entry is not None:
    raise ValidationError(ERROR_MSG["exist"].format(value))
