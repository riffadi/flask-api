from flask import jsonify, Blueprint, abort
from flask_restful import Resource,Api, reqparse, fields, marshal, marshal_with
from hashlib import md5

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


import models

user_fields = {
	'username' : fields.String,
	'access_token' : fields.String,
}

class UserBase(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help = 'Username wajib ada',
			location = ['form', 'json']
		)
		self.reqparse.add_argument(
			'password',
			required=True,
			help = 'Password wajib ada',
			location = ['form', 'json']
		)
		super().__init__()


class UserList(UserBase):

	def post(self):
		args = self.reqparse.parse_args()
		username = args.get('username')
		password = args.get('password')
		try:
			models.User.select().where(models.User.username == username).get()
		except models.User.DoesNotExist:
			user = models.User.create(
				username = username,
				password = md5(password.encode('utf-8')).hexdigest()
			)
			#send token
			access_token = create_access_token(identity = username)
			user.access_token = access_token
			return marshal(user, user_fields)
		else:
			raise Exception('Username sudah terdaftar')

	@jwt_required
	def get(self):
		return {'message' : 'ini bagian yang terproteksi'}


class User(UserBase):


	def post(self):
		args = self.reqparse.parse_args()
		username = args.get('username')
		password = args.get('password')
		try:
			hashPass = md5(password.encode('utf-8')).hexdigest()
			user = models.User.get((models.User.username == username) &
						 (models.User.password == hashPass))
		except models.User.DoesNotExist:
			return {'messages' : 'User or Password is wrong!'}
		else:
			access_token = create_access_token(identity = username)
			return {'messages' : 'You have successfully signin ', 'access_token': access_token}



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(UserList, '/user/register', endpoint='user/register')
api.add_resource(User, '/user/signin', endpoint='user/signin')

