from peewee import *

db = SqliteDatabase('links.db')

class Links(Model):
	id = PrimaryKeyField()
	title = CharField()
	href = TextField()
	categorie = TextField()
	nb_aside = TextField()
	class Meta:
		database = db

def initialize_db():
	db.connect()
	db.create_tables([Links],safe=True)