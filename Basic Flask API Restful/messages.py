from flask import jsonify
from flask_restful import Resource

import models

class MessageList(Resource):
	def get(self):
		#ambil data dari database
		messages = models.Message.select()
		return jsonify({'messages' : messages})

