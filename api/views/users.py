"""Module for users resource"""

from main import api

from flask_restplus import Resource
from flask import request

from api.models import User
from api.serializers.users import UserSchema


@api.route('/users/')
class UserResource(Resource):
    def get(self):
        return {'status': 'success', 'message': 'working'}
