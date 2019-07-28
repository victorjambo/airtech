"""Module with constant messages"""

SUCCESS_MSG = {
    "created": "{} successfully created",
    "fetched": "{} fetched successfully",
    "deleted": "{} successfully deleted",
    "updated": "{} successfully updated",
    "register": "{} successfully registered",
    "reset_password": "Reset Password Success",
    "login": "Login Success",
}

ERROR_MSG = {
  "required": "This field is required",
  "password": "Provide a Stronger Password",
  "exist": "user with `{}` already exist",
  "not_found": "{} not found",
  "auth": "username and password do not match",
  "invalid_id": "invalid id",
  "invalid_date": "invalid date time format, example of valid date `2019-06-24` or `2019-07-28 10:15:20`",
  "past_date": "Cannot create ticket with date older than today"
}

jwt_errors = {
  "INVALID_TOKEN_MSG": "Authorization failed due to an Invalid token.",
  "EXPIRED_TOKEN_MSG": "Token expired. Please login to get a new token",
  "NO_BEARER_MSG": "Bad request. The token should begin with the word 'Bearer'.",
  "NO_TOKEN_MSG": "Bad request. Header does not contain an authorization token."
}
