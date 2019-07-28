import jwt
from os import getenv
from datetime import datetime
from base64 import b64encode, b64decode, encode

from api.models import User
from tests.mock.users import user_data
from api.utilities.constants import CHARSET


def generate_token(exp=None):
    """Generates jwt tokens for testing
    """

    secret_key = getenv('SECRET')

    user = User.query.filter_by(username="victor").first()
    if not user:
      user = User(**user_data["victor"]).save()

    user_data["victor"]["id"] = user.id
    payload = {'data': user_data["victor"]}
    payload.__setitem__('exp', exp) if exp is not None else ''
    token = jwt.encode(payload, secret_key).decode(CHARSET)
    return 'Bearer {0}'.format(token)