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

@mod_web.route("/sponsors", methods = ["GET"])
def sponsors():
    return mod_web.send_static_file("prospectus.pdf")

@mod_web.route("/sponsors.pdf", methods = ["GET"])
@mod_web.route("/sponsor.pdf", methods = ["GET"])
@mod_web.route("/sponsor", methods = ["GET"])
def foward_sponsors():
    return redirect("/sponsors")

@mod_web.route("/livestream", methods = ["GET"])
def livestream():
	return redirect("https://livestream.com/accounts/18225475/hackbca")