from flask import render_template, redirect, url_for, request, flash, session
from . import user_module as mod_user
from . import controllers as controller
from .forms import *
from application import cache
from application import CONFIG

@mod_user.route('/index')
def index():
	return render_template("user.index.html")

@mod_user.route("/register", methods = ["GET", "POST"])
def register():
	# if current_user.is_authenticated:
	# 	return redirect("/account")

	# if not CONFIG["HACKER_REGISTRATION_ENABLED"]:
	# 	flash("Registration is not open at this time.", "error")
	# 	return redirect("/")

	form = RegistrationForm(request.form)
	if request.method == "POST" and form.validate():
		# try:
		controller.add_user(request.form["email"], request.form["first_name"], request.form["last_name"], request.form["password"], request.form["school"], request.form["gender"], request.form["beginner"], request.form["ethnicity"], request.form["grade"], request.form["num_hackathons"], request.form["link1"], request.form["link2"], request.form["link3"], request.form["t_shirt_size"], request.form["free_response1"], request.form["food_allergies"], request.form["mlh_terms"])
		# flash("Check your inbox for an email to confirm your account!", "success")
		# except Exception as e:
		# 	exceptionType = e.args[0]
		# 	if exceptionType == "UserExistsError":
		# 		flash("A user with that email already exists.", "error")
		# 	else:
		# 		if CONFIG["DEBUG"]:
		# 			raise e
		# 		else:
		# 			flash("Something went wrong.", "error")
		return redirect(url_for('user.register'))
	return render_template("user.register.html", form = form)

	