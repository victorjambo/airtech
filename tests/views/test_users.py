"""Module of tests for user endpoints"""
import os

from flask import json
from unittest.mock import Mock
from cloudinary import uploader
from tempfile import TemporaryFile
from io import BytesIO
from werkzeug import FileStorage

from api.models import User
from tests.mock.users import user_data
from api.utilities.constants import CHARSET
from api.utilities.messages import SUCCESS_MSG, ERROR_MSG

BASE_URL = os.getenv('API_BASE_URL_V1', default="/api/v1")


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



class TestAuthLoginResource:
  """Test AuthLoginResource POST endpoint
  """

  def test_login_with_valid_data_succeeds(self, client, init_db, auth_header):
    """Test successfully login
    """
    victor = user_data["victor"]
    del victor["email"]
    data = json.dumps(victor)
    response = client.post(f'{BASE_URL}/auth/login', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == SUCCESS_MSG["login"]

  def test_login_with_wrong_username_fails(self, client, init_db, auth_header):
    """Test fails login username
    """

    data = json.dumps({
      "username": "invalid",
      "password": "invalid"
    })
    response = client.post(f'{BASE_URL}/auth/login', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 404
    assert response_json["status"] == "error"
    assert response_json["message"] == ERROR_MSG["not_found"].format("User")

  def test_login_with_wrong_password_fails(self, client, init_db, auth_header):
    """Test fails login password
    """

    victor = user_data["victor"]
    victor["password"] = "invalid"

    data = json.dumps(victor)
    response = client.post(f'{BASE_URL}/auth/login', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 401
    assert response_json["status"] == "error"
    assert response_json["message"] == "username and password do not match"  # TODO


class TestUserUploadResource:
  """Test UserUploadResource POST endpoint
  """

  def test_upload_image_with_valid_data_succeeds(self, client, init_db, auth_header_token, cloudinary_mock_response):
    """test
    """

    uploader.upload = Mock(side_effect=lambda *args: cloudinary_mock_response)

    filehandle = FileStorage(stream=BytesIO(b'avatar.png'))
    data = {'image': open('tests/views/avatar.png', 'rb')}

    response = client.post(
      f'{BASE_URL}/users/upload',
      data=data,
      headers=auth_header_token,
      content_type='multipart/form-data')

    print(response.data)
