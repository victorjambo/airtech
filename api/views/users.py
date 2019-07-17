"""Module for users resource"""

from main import api

from flask_restplus import Resource
from flask import request
from passlib.hash import sha256_crypt

from api.models import User
from api.serializers.users import UserSchema, UserSignupSchema
from api.utilities.messages import SUCCESS_MSG
from api.utilities.generate_token import generate_token
from api.middlewares.base_validator import ValidationError


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

        request_data = request.get_json()

        user_schema = UserSchema(only=["username", "password"])
        user_data = user_schema.load_object_into_schema(request_data)

        user = User.get_username_or_404(user_data["username"])

        token, error = generate_token(user, user_data)

        if error:
            return ValidationError(error).to_dict(), 401

        return {
            "status": "success",
            "message": SUCCESS_MSG["login"],
            "token": token
        }, 200
