"""validate resource id from url"""

import re
from functools import wraps

from api.middlewares.base_validator import ValidationError
from api.utilities.messages import ERROR_MSG


def is_id_valid(id):
  """Regex match if id is valid
  """
  return re.match(r'^[\-a-zA-Z0-9_]+\Z', id)


def validate_id(func):
  """Decorator to validate id
  """

  @wraps(func)
  def decorated_function(*args, **kwargs):
      check_id_valid(**kwargs)
      return func(*args, **kwargs)

  return decorated_function

def check_id_valid(**kwargs):
  for key in kwargs:
    if key.endswith("_id") and not is_id_valid(kwargs.get(key, None)):
      raise ValidationError({
        "status": "error",
        "message": ERROR_MSG["invalid_id"]
      }, 400)
