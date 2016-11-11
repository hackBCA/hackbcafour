# from flask import render_template, request, redirect, url_for
# from application import app
# from .forms import *
# from . import controllers as controller


# @app.route("/")
# @app.route("/index")
# def index():
# 	return render_template('index.html')


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
	return render_template('index.html', form=form)
 
