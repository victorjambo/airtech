"""Module of tests for user endpoints"""
from os import getenv

from flask import json

from api.models import User
from tests.mock.users import user_data
from api.utilities.constants import CHARSET
from api.utilities.messages import SUCCESS_MSG, ERROR_MSG

BASE_URL = getenv('API_BASE_URL_V1', default="/api/v1")


class TestAuthSignupResource:
  """Test AuthSignupResource POST endpoint
  """

  def test_signup_with_valid_data_succeeds(self, client, init_db, auth_header):
    """Test successfully signup
    """
    data = json.dumps(user_data["victor"])
    response = client.post(f'{BASE_URL}/auth/signup', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 201
    assert response_json["status"] == "success"
    assert response_json["message"] == SUCCESS_MSG["register"].format("User")

  def test_signup_duplicate_user_email_fails(self, client, init_db, auth_header):
    """Test duplicate signup
    """
    data = json.dumps(user_data["victor"])
    response = client.post(f'{BASE_URL}/auth/signup', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["_schema"][0] == ERROR_MSG["exist"].format(user_data["victor"]["email"])

  def test_signup_duplicate_user_username_fails(self, client, init_db, auth_header):
    """Test duplicate username signup
    """
    user_data["victor"]["email"] = "user@example.com"
    data = json.dumps(user_data["victor"])
    response = client.post(f'{BASE_URL}/auth/signup', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["_schema"][0] == ERROR_MSG["exist"].format(user_data["victor"]["username"])

  def test_create_user_with_invalid_email_fails(self, client, init_db, auth_header):
    """Test create user when user data is invalid
    """
    user_data["victor"]["email"] = "invalid"
    data = json.dumps(user_data["victor"])
    response = client.post(f'{BASE_URL}/auth/signup', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["email"][0] == "Not a valid email address."

  def test_create_user_with_invalid_password_fails(self, client, init_db, auth_header):
    """Test create user when user data is invalid
    """
    user_data["mutai"]["password"] = "pass"
    data = json.dumps(user_data["mutai"])
    response = client.post(f'{BASE_URL}/auth/signup', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["password"][0] == "Provide a Stronger Password"
