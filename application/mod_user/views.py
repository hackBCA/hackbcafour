from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import user_module as mod_user
from . import controllers as controller
from .forms import *
from application import cache
from application import CONFIG


@cache.cached()
@mod_user.route("/login", methods = ["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect("/account")

  form = LoginForm(request.form)
  if request.method == "POST" and form.validate():
    try:
      if controller.verify_user(request.form["email"], request.form["password"]) is None:
        flash("Invalid email and/or password.", "error")
      else:
        confirmed = controller.get_user_attr(request.form["email"], "confirmed")

        if not confirmed:
          session["email"] = request.form["email"]
          return redirect("/account/confirm")
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

@mod_user.route("/logout", methods = ["GET", "POST"])
def logout():
	controller.logout()
	return redirect("/")

@cache.cached()
@mod_user.route("/forgot", methods = ["GET", "POST"])
def recover():
  if current_user.is_authenticated:
    return redirect("/account")
  form = EmailForm(request.form)
  if request.method == "POST" and form.validate():
    try:
      controller.send_recovery_email(request.form["email"])
      flash("Email sent to " + request.form["email"] + '.', 'success')
    except Exception as e:
      exceptionType = e.args[0]
      if exceptionType == "UserDoesNotExistError":
        flash("No account exists with that email.", "error")
      else:
        if CONFIG["DEBUG"]:
          raise e
        else:
          flash("Something went wrong.", "error")
  return render_template("user.forgot.html", form = form)

@mod_user.route("/recover/<token>", methods = ["GET", "POST"])
def recover_change(token):
  email = controller.detokenize_email(token)

  form = RecoverForm(request.form)
  if request.method == "POST" and form.validate():
    try:
      controller.change_password(email, request.form["password"])
      flash("Password changed.", "success")
      return redirect("/")
    except Exception as e:
      if CONFIG["DEBUG"]:
        raise e
      else:
        flash("Something went wrong.", "error")
  return render_template("user.recover.html", email = email, form = form)

@mod_user.route("/account")
@login_required
def account():
  return render_template("user.account.html")


@mod_user.route("/account/confirm", methods = ["GET", "POST"])
def verify():
  if "email" not in session:
    return redirect("/")

  email = session["email"]

  if request.method == "POST":
    controller.validate_email(email)
    flash("Almost there! Confirmation email resent.", "neutral")
    return redirect("/login")

  controller.logout();

  confirmed = controller.get_user_attr(email, "confirmed")

  return render_template("user.confirm.html")

@mod_user.route("/account/confirm/<token>")
def confirm_email(token):
  session.pop("email", None)
  controller.confirm_email(token)
  flash("Account confirmed! Login to start your application!", "success")
  return redirect("/index")

@mod_user.route("/account/settings", methods = ["GET", "POST"])
@login_required
def settings():
  name_form = ChangeNameForm(request.form)
  password_form = ChangePasswordForm(request.form)
  if request.method == "POST":
    if request.form["setting"] == "name" and name_form.validate():
      try:
        controller.change_name(current_user.email, request.form["firstname"], request.form["lastname"])
        flash("Name changed.", "success")
      except Exception as e:
        if CONFIG["DEBUG"]:
          raise e
        else:
          flash("Something went wrong.", "error")
    if request.form["setting"] == "password" and password_form.validate():
      if controller.verify_user(current_user.email, request.form["password"]) is not None:
        try:
          controller.change_password(current_user.email, request.form["new_password"])
          flash("Password changed.", "success")
        except Exception as e:
          if CONFIG["DEBUG"]:
            raise e
          else:
            flash("Something went wrong.", "error")
      else:
        flash("Incorrect password.", "error")

    if request.form["setting"] == "delete_account":
      try:
        controller.delete_account(current_user.email)
        flash("Account deleted.", "success")
        return redirect("/")
      except Exception as e:
        if CONFIG["DEBUG"]:
          raise e
        else:
          flash("Something went wrong.", "error")
  else:
    user = controller.get_user(current_user.email)
    name_form = ChangeNameForm(request.form, obj = user)
  return render_template("user.settings.html", name_form = name_form, password_form = password_form)

@cache.cached()
@mod_user.route("/register", methods = ["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect("/account")

  ####### Below code: changed from form to a hrefs => mentor & hackers opened at the same time
  # if not CONFIG["REGISTRATION_ENABLED"]:
	 #  flash("Registration is not open at this time.", "error")
	 #  return redirect("/")

  # form = RegistrationForm(request.form)
  # if request.method == "POST" and form.validate():
  #   type_account = request.form["type_account"]

  #   if type_account == "hacker":
  #     if CONFIG["HACKER_REGISTRATION_ENABLED"]:
  #       return redirect("/register/hacker")
  #     else:
  #       flash("Hacker registration is not open at this time.", "error")
  #       return render_template("user.register.html", form = form)
  #   elif type_account == "mentor":
  #     if CONFIG["MENTOR_REGISTRATION_ENABLED"]:
  #       return redirect("register/mentor")
  #     else:
  #       flash("Mentor registration is not open at this time.", "error")
  #       return render_template("user.register.html", form = form)
  # return render_template("user.register.html", form = form)
  return render_template("user.register.html")



@cache.cached()
@mod_user.route("/register/hacker", methods = ["GET", "POST"])
def hacker_registration():
  if current_user.is_authenticated:
    return redirect("/account")
  elif not CONFIG["REGISTRATION_ENABLED"]:
    flash("Registration is not open at this time.", "error")
    return redirect("/")

  if CONFIG["HACKER_REGISTRATION_ENABLED"]:
    form = HackerRegistrationForm(request.form) 

    if request.method == "POST" and form.validate():
      try:
        email = request.form['email']
        password = request.form['password']

        fields = { 'email':email, 'first_name':request.form["first_name"], 'last_name':request.form["last_name"], 'school':request.form["school"], 'gender':request.form["gender"], 'beginner':request.form["beginner"], 'ethnicity':request.form["ethnicity"], 'grade':request.form["grade"], 'age':request.form["age"], 'num_hackathons':request.form["num_hackathons"], 'free_response1':request.form["free_response1"], 'link1':request.form["link1"], 'link2':request.form["link2"], 'link3':request.form["link3"], 'mlh_coc':request.form["mlh_coc"], 'mlh_terms':request.form["mlh_terms"] }

        controller.add_hacker(fields, email, password)
        flash("Check your inbox for an email to confirm your account!", "success")
        return redirect("/")
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
  else:
    flash("Hacker registration is not open at this time.", "error")
    return redirect(url_for("user.register"))
  return render_template("user.hacker.html", form=form)


@cache.cached()
@mod_user.route("/register/mentor", methods = ["GET", "POST"])
def mentor_registration():
  if current_user.is_authenticated:
    return redirect("/account")
  elif not CONFIG["REGISTRATION_ENABLED"]:
    flash("Registration is not open at this time.", "error")
    return redirect("/")

  if CONFIG["MENTOR_REGISTRATION_ENABLED"]:
    form = MentorRegistrationForm(request.form)
    
    if request.method == "POST" and form.validate():
      try:
        email = request.form['email']
        password = request.form['password']

        fields = { 'email':email, 'first_name':request.form["first_name"], 'last_name':request.form["last_name"], 'school':request.form["school"], 'phone':request.form["phone"], 'num_hackathons':request.form["num_hackathons"], 'mentor_free_response1':request.form["mentor_free_response1"], 'mentor_free_response2':request.form["mentor_free_response2"], 'github_link':request.form["github_link"], 'linkedin_link':request.form["linkedin_link"], 'site_link':request.form["site_link"], 'other_link':request.form["other_link"], 'mlh_coc':request.form["mlh_coc"], 'mlh_terms':request.form["mlh_terms"] }

        controller.add_mentor(fields, email, password)
        flash("Check your inbox for an email to confirm your account!", "success")
        return redirect("/")
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
  else:
    flash("Mentor registration is not open at this time.", "error")
    return redirect(url_for("user.register"))
  return render_template("user.mentor.html", form=form)




	

