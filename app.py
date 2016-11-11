from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

MONGOLAB_URL = ""
client = MongoClient(MONGOLAB_URL)

db = client.get_default_database()
mailing_list = db.mailing_list

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		email_string = request.form['email']
		email_address = {'email_address': email_string}

		mailing_list.insert(email_address)

		return redirect('/')

	return render_template('index.html')

if __name__ == "__main__":
	app.run()