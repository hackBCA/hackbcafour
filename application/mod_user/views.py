from flask import *
from . import user_module as mod_user
# from . import controllers
from application import cache

@mod_user.route('/index')
def index():
	return render_template("user.index.html")
