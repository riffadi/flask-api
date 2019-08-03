from flask import Flask, request
from flask_restful import Resource, Api
from resources.messages import messages_api

import models


class  user:
	pass


users_api = Blueprint('resources.users', __name__)
api = Api(messages_api)

api.add_resource(Users, '/users', endpoint='users')
