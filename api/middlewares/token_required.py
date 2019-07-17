import jwt
import os
from functools import wraps
from flask import jsonify, request

from .base_validator import ValidationError
from api.utilities.messages import jwt_errors


def token_required(f):
  """Ensures user is logged in before action
  Checks of token is provided in header
  decodes the token then returns current user info
  """
  @wraps(f)
  def wrap(*args, **kwargs):
    token = request.headers.get('Authorization')

    if not token:
      raise ValidationError({'message': jwt_errors['NO_TOKEN_MSG']}, 401)
    elif 'bearer' not in token.lower():
      raise ValidationError({'message': jwt_errors['NO_BEARER_MSG']}, 401)

    token = token.split(' ')[-1]

    try:
      public_key = os.getenv("SECRET")
      decoded_token = jwt.decode(token, public_key, algorithms=["HS256"], verify=True)
      current_user = decoded_token["data"]
    except jwt.ExpiredSignatureError:
      raise ValidationError({'message': jwt_errors['EXPIRED_TOKEN_MSG']}, 401)
    except (jwt.DecodeError, jwt.InvalidAlgorithmError):
      raise ValidationError({'message': jwt_errors['INVALID_TOKEN_MSG']}, 401)

    setattr(request, 'decoded_token', decoded_token)
    return f(*args, **kwargs)
  return wrap
