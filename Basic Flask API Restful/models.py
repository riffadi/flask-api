import datetime

from peewee import *

DATABASE = SqliteDatabase('api.db')

class Message(Model):
	content = TextField()
	datetime = DateTimeField(default=datetime.datetime.now())


	class Meta:
		database = DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Message])
	DATABASE.close()