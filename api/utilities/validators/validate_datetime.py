"""Validate DateTime for tickets"""
import re
import datetime
from marshmallow import ValidationError

from api.utilities.messages import ERROR_MSG

DATETIME_REGEX = re.compile(r"^(?=\d)(?:(?:1[6-9]|[2-9]\d)?\d\d([-.\/])(?:1[012]|0?[1-9])\1(?:31(?<!.(?:0[2469]|11))|(?:30|29)(?<!.02)|29(?=.0?2.(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(?:\x20|$))|(?:2[0-8]|1\d|0?[1-9]))(?:(?=\x20\d)\x20|$))?(((0?[1-9]|1[012])(:[0-5]\d){0,2}(\x20[AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$", re.I | re.UNICODE)

def validate_datetime(obj):
  """Validate datetime is a valid time
  """

  if not DATETIME_REGEX.match(obj.strip()):
    raise ValidationError(ERROR_MSG["invalid_date"])

def validate_past_dates(obj):
  """validate past datetime
  """

  dt = convert_datetime(obj)
  if dt <= datetime.datetime.now():
    raise ValidationError(ERROR_MSG["past_date"])

def convert_datetime(obj):
  """Convert string to date
  """
  date_format = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']
  REGEX = [
    re.compile(r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}$", re.I | re.UNICODE),
    re.compile(r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}$", re.I | re.UNICODE),
    re.compile(r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$", re.I | re.UNICODE)
  ]

  if REGEX[0].match(obj.strip()):
    return datetime.datetime.strptime(obj, date_format[0])
  elif REGEX[1].match(obj.strip()):
    return datetime.datetime.strptime(obj, date_format[1])
  elif REGEX[2].match(obj.strip()):
    return datetime.datetime.strptime(obj, date_format[2])
  else:
    raise ValidationError(obj)
