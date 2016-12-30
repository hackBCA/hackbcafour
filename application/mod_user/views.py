from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import user_module as mod_user
from . import controllers as controller
from .forms import *
from application import cache
from application import CONFIG

@mod_user.route('/index')
def index():
	return render_template("user.index.html")


@cache.cached()
@mod_user.route("/login", methods = ["GET", "POST"])
def login():
  # if current_user.is_authenticated:
  #   return redirect("/account")

  form = LoginForm(request.form)
  if request.method == "POST" and form.validate():
    try:
      if controller.verify_user(request.form["email"], request.form["password"]) is None:
        flash("Invalid email and/or password.", "error")
      else:
        confirmed = controller.get_user_attr(request.form["email"], "confirmed")

        if not confirmed:
          session["email"] = request.form["email"]
          return redirect("/index")
        else:
          controller.login(request.form["email"])
          if request.args.get("next") is not None:
            return redirect(request.args.get("next"))
          return redirect("/account")
    except Exception as e:
      if(CONFIG["DEBUG"]):
        raise e
      else:
        flash("Something went wrong.", "error")
  return render_template("user.login.html", form = form)

@cache.cached()
@mod_user.route("/register", methods = ["GET", "POST"])
def register():
	# if current_user.is_authenticated:
	# 	return redirect("/account")

	# if not CONFIG["HACKER_REGISTRATION_ENABLED"]:
	# 	flash("Registration is not open at this time.", "error")
	# 	return redirect("/")

	form = RegistrationForm(request.form)
	if request.method == "POST" and form.validate():
		try:
			controller.add_user(request.form["email"], request.form["first_name"], request.form["last_name"], request.form["password"], request.form["school"], request.form["gender"], request.form["beginner"], request.form["ethnicity"], request.form["grade"], request.form["num_hackathons"], request.form["link1"], request.form["link2"], request.form["link3"], request.form["t_shirt_size"], request.form["free_response1"], request.form["food_allergies"], request.form["mlh_terms"])
			flash("Check your inbox for an email to confirm your account!", "success")
		except Exception as e:
			print(e)
			exceptionType = e.args[0]
			if exceptionType == "UserExistsError":
				flash("A user with that email already exists.", "error")
			else:
				if CONFIG["DEBUG"]:
					raise e
				else:
					flash("Something went wrong.", "error")
		return redirect(url_for('user.register'))
	return render_template("user.register.html", form = form)

@mod_user.route("/account/confirm/<token>")
def confirm_email(token):
  session.pop("email", None)
  controller.confirm_email(token)
  flash("Account confirmed! Login to start your application!", "success")
  return redirect("/index")

	
@mod_user.route("/account")
@login_required
def account():
  return render_template("user.account.html")
