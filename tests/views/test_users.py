"""Module of tests for user endpoints"""
import os

import cloudinary
from flask import json
from unittest.mock import Mock
from tempfile import TemporaryFile
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

  def test_login_with_empty_username_fails(self, client, init_db, auth_header):
    """Test fails login username
    """

    data = json.dumps({
      "username": "",
      "password": ""
    })
    response = client.post(f'{BASE_URL}/auth/login', headers=auth_header, data=data)
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["errors"]["username"] == [ERROR_MSG["required"]]
    assert response_json["errors"]["password"] == [ERROR_MSG["required"]]

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

  def test_upload_image_succeeds(self, client, init_db, auth_header_token):
    """test upload image
    """
    mock_response = {
      'public_id': 'public-id',
      'url': 'http://test.com/test'
    }
    cloudinary.uploader.upload = Mock(side_effect=lambda *args: mock_response)

    data = dict(image=open('tests/mock/avatar.png', 'rb'))

    response = client.post(
      f'{BASE_URL}/users/upload',
      headers=auth_header_token,
      data=data,
      content_type='multipart/form-data')
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Image uploaded"

  def test_update_image_succeeds(self, client, init_db, auth_header_token):
    """test upload image
    """
    mock_response = {
      'public_id': 'public-id',
      'url': 'http://test.com/test'
    }
    cloudinary.uploader.upload = Mock(side_effect=lambda *args: mock_response)
    cloudinary.uploader.destroy = Mock(side_effect=lambda *args: mock_response)

    data = dict(image=open('tests/mock/avatar.png', 'rb'))

    response = client.post(
      f'{BASE_URL}/users/upload',
      headers=auth_header_token,
      data=data,
      content_type='multipart/form-data')
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Image uploaded"

  def test_delete_image_succeeds(self, client, init_db, auth_header_token):
    """test delete upload image
    """
    mock_response = {'result': 'ok'}
    cloudinary.uploader.destroy = Mock(side_effect=lambda *args: mock_response)

    response = client.delete(
      f'{BASE_URL}/users/upload',
      headers=auth_header_token,
      content_type='multipart/form-data')
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Image deleted"

  def test_upload_non_image_file_fails(self, client, init_db, auth_header_token):
    """test upload image fails
    """
    data = dict(image=open('tests/mock/upload.txt', 'rb'))

    response = client.post(
      f'{BASE_URL}/users/upload',
      headers=auth_header_token,
      data=data,
      content_type='multipart/form-data')
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["message"] == "File type not supported, type must be either 'jpg', 'jpeg', 'png', 'gif'"

  def test_upload_no_image_fails(self, client, init_db, auth_header_token):
    """test upload image fails
    """
    data = dict(image="")

    response = client.post(
      f'{BASE_URL}/users/upload',
      headers=auth_header_token,
      data=data,
      content_type='multipart/form-data')
    response_json = json.loads(response.data.decode(CHARSET))

    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert response_json["message"] == "Image is required"

