"""Module for users resource"""
import os
from main import api

from flask_restplus import Resource
from flask import request
from passlib.hash import sha256_crypt
from random import randint
from sqlalchemy import sql
from main import cache

from api.models import User
from api.serializers.users import UserSchema, UserSignupSchema
from api.utilities.messages import SUCCESS_MSG
from api.utilities.generate_token import generate_token
from api.middlewares.base_validator import ValidationError
from api.utilities.helpers.cloudinary import Cloud
from api.middlewares.token_required import token_required

FLASK_ENV = os.getenv('FLASK_ENV', default='development')


@api.route("/auth/signup")
class AuthSignupResource(Resource):
    def post(self):
        """signup endpoint
        """

        request_data = request.get_json()

        user_schema = UserSignupSchema()
        user_data = user_schema.load_object_into_schema(request_data)

        user_data["password"] = sha256_crypt.hash(str(user_data["password"]))

        user = User(**user_data)
        user.save()

        data = user_schema.dump(user).data
        del data["password"]

        return {
            "status": "success",
            "message": SUCCESS_MSG["register"].format("User"),
            "data": data
        }, 201


@api.route("/auth/login")
class AuthLoginResource(Resource):
    def post(self):
        """login endpoint
        """
        mapper = {
            'testing': self.get_user_testing,
            'development': self.get_user,
            'production': self.get_user
        }

        request_data = request.get_json()

        user_schema = UserSchema(only=["username", "password"])
        user_data = user_schema.load_object_into_schema(request_data)

        user = mapper[FLASK_ENV](user_data["username"])

        token, error = generate_token(user, user_data)

        if error:
            return ValidationError(error).to_dict(), 401

        return {
            "status": "success",
            "message": SUCCESS_MSG["login"],
            "token": token
        }, 200

    @cache.cached(timeout=50, key_prefix='get_user')
    def get_user(self, username):
        return User.get_username_or_404(username)

    def get_user_testing(self, username):
        return User.get_username_or_404(username)

@api.route("/users/upload")
class UserUploadResource(Resource, Cloud):
    @token_required
    def post(self):
        """upload image endpoint
        """
        ALLOWED_TYPES = ['jpg', 'jpeg', 'png', 'gif']
        user_id = request.decoded_token["data"]["id"]
        user = User.get_or_404(user_id)

        if user.image:
            res = self.delete_image(user.image["public_id"])

        image = request.files.get('image', default=False)
        if not image:
            return {
                "status": "error",
                "message": "Image is required",
            }, 400

        extension = image.filename.split('.')[-1]
        if extension not in ALLOWED_TYPES:
            return {
                "status": "error",
                "message": "File type not supported, type must be either 'jpg', 'jpeg', 'png', 'gif'",
            }, 400

        res = self.upload_image(image)

        user.update_(**{
            "image": {
                "url": res["url"],
                "public_id": res["public_id"]
            }
        })

        user_schema = UserSchema(exclude=["password"])
        data = user_schema.dump(user).data

        return {
            "status": "success",
            "message": "Image uploaded",
            "data": data
        }, 200

    @token_required
    def delete(self):
        user_id = request.decoded_token["data"]["id"]
        user = User.get_or_404(user_id)

        self.delete_image(user.image["public_id"])
        user.update_(**{
            "image": sql.null()
        })

        user_schema = UserSchema(exclude=["password"])
        data = user_schema.dump(user).data

        return {
            "status": "success",
            "message": "Image deleted",
            "data": data
        }, 200
