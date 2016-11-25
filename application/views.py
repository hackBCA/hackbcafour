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
	return render_template('index.html', form=form)

@app.route("/sponsors", methods = ["GET"])
def sponsors():
    return app.send_static_file("prospectus.pdf")

@app.route("/sponsors.pdf", methods = ["GET"])
@app.route("/sponsor.pdf", methods = ["GET"])
@app.route("/sponsor", methods = ["GET"])
def foward_sponsors():
    return redirect("/sponsors")