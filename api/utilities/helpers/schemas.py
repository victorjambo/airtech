"""Schema helpers"""

from api.utilities.messages import ERROR_MSG

def default_args(**kwargs):
  """Marshmallow fields
  """

  return {
    "required": True,
    "validate": kwargs.get("validate"),
    "error_messages": {
      "required": ERROR_MSG["required"]
    }
  }
