from application import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import flash

def add_list(email):
	client = MongoClient(app.config['MONGOLAB_URL'])
	db = client.get_default_database()
	mailing_list = db.mailing_list

	if (mailing_list.find_one({"email_address": email})):
		flash('Email already exists.')
	else:
		email_address = {'email_address': email}
		mailing_list.insert(email_address)
		flash('Awesome! You\'ll hear from us soon.')
	
