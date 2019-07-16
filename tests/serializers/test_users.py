"""Module for testing permission schema"""
import pytest

from api.serializers.users import UserSchema
from tests.mock.users import user_data


class TestUserSchema:
  """Test user schema
  """

  def test_user_schema_with_valid_data_succeeds(self, init_db):
    """Should pass when valid permission type is supplied
    """
    user_schema = UserSchema()
    data = user_schema.load_object_into_schema(user_data["victor"])

    assert data['username'] == user_data["victor"]['username']
