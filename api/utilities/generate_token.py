import jwt
import os
import datetime
from api.utilities.constants import CHARSET
from passlib.hash import sha256_crypt
from api.utilities.messages import ERROR_MSG


def generate_token(user, user_data):
  """This method generates a jwt token on login
  it authenticates/validate the user
  returns token
  """
  password = user.password
  candidate_password = user_data["password"]

  if sha256_crypt.verify(candidate_password, password):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode(
      {
        "data": {
          "id": user.id,
          "email": user.email,
          "username": user.username
        },
        "exp": exp_time
      }, os.getenv("SECRET")
    )
    return token.decode(CHARSET), False
  return False, {"message": ERROR_MSG["auth"]}
