"""Module for dynamic filters and advanced queries"""
from re import sub


class Filters:
  """Filter class
  """
  def __init__(self, model):
    self.model = model

  def filter_query(self, args):
    """filter
    """

    results = {}
    for k, v in args.to_dict().items():
      results[self.to_snake_case(k)] = v

    return self.model.query.filter_by(**results)

  def to_snake_case(self, string):
    """Converts camelCase to snake_case
    """

    return sub(r'(.)([A-Z])', r'\1_\2', string).lower()
