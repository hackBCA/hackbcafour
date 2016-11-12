from application import app
from pymongo import MongoClient
from bson.objectid import ObjectId

def add_list(email):
	client = MongoClient(app.config['MONGOLAB_URL'])
	db = client.get_default_database()
	mailing_list = db.mailing_list

	email_address = {'email_address': email}
	mailing_list.insert(email_address)

