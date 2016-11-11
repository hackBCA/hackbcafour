from flask import render_template, request, redirect, url_for
from application import app
from .forms import *
from . import controllers as controller


@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')
