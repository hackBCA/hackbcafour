from flask import render_template, request, flash, redirect, url_for
from application import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from .forms import *
from . import controllers as controller


@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
	form = MailList()
	if request.method == 'POST':
			controller.add_list(request.form['email'])			
			flash('Thanks for registering, we\'ll keep you updated.')
			return redirect(url_for("index"))

	return render_template('index.html', form=form)