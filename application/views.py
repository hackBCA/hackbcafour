from flask import render_template, request, redirect, url_for
from application import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from .forms import *
from . import controllers as controller


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
	form = MailList()
	if request.method == 'POST':
			controller.add_list(request.form['email'])
			return redirect('/')
	return render_template('index.html', form=form)