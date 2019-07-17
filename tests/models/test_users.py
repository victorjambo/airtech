"""Test User Model Module"""

from api.models import User


class TestUserModelClass:
  """Test UserModel
  """
  def test_new_user(self, init_db, new_user):
    """Test create new user
    """
    user = new_user
    assert user == new_user.save()

  def test_count(self):
    """Test model data count
    """
    assert User.count() == 1

  def test_query(self):
    """Test querying user works
    """
    user_query = User.query_()
    assert user_query.count() == 1
    assert isinstance(user_query.all(), list)

  def test_update(self, new_user):
    """test update user model
    """
    new_user.update_(username='Modified')
    assert new_user.username == 'Modified'

  def test_delete(self, new_user):
    """test delete user model
    """
    new_user.delete()
    assert User.get(new_user.id) is None

  def test_user_model_string_representation(self, new_user):
    """Should compute the string representation of a user
    """
    assert repr(new_user) == f'<User {new_user.username}>'
