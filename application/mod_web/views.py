from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import web_module as mod_web
from . import controllers as controller
from application import cache
from application import CONFIG

@cache.cached()
@mod_web.route('/index', methods = ["GET", "POST"])
@mod_web.route('/')
def index():
	return render_template("web.index.html")

