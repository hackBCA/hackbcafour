from application import CONFIG, app
from .models import *
from flask_login import login_user, logout_user
import bcrypt
import re
import sendgrid
import time
import requests
import json
from itsdangerous import URLSafeTimedSerializer


AuthenticationError = Exception("AuthenticationError", "Invalid credentials.")
UserExistsError = Exception("UserExistsError", "Email already exists in database.")
UserDoesNotExistError = Exception("UserDoesNotExistError", "Account with given email does not exist.")
GenericMongoError = Exception("GenericMongoError")

def add_user(email, firstname, lastname, password, school, gender, beginner, ethnicity, grade, num_hackathons, link1, link2, link3, t_shirt_size, free_response1, food_allergies, mlh_terms):
	existingUser = get_user(email)
	if existingUser is not None:
		raise UserExistsError
	
	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
	new_entry = UserEntry(email = email.lower(), hashed = hashed, firstname = firstname, lastname = lastname, type_account = "hacker", school = school, gender = gender, beginner = beginner, ethnicity = ethnicity, grade = grade, num_hackathons = num_hackathons, link1 = link1, link2 = link2, link3 = link3, t_shirt_size = t_shirt_size, free_response1 = free_response1, food_allergies = food_allergies, mlh_terms = mlh_terms)
	new_entry.save()
	
	# validate_email(email)
	hello = "hello"


def get_user(email):
	try:
		entries = UserEntry.objects(email = email.lower())
		if entries.count() == 1:
			return entries[0]
		return None
	except Exception:
		raise GenericMongoError



def validate_email(email):
	token = tokenize_email(email)

	message = sendgrid.Mail()
	message.add_to(email)
	message.set_from("contact@hackbca.com")
	message.set_subject("hackBCA III - Account Creation Confirmation")
	message.set_html("<p></p>")

	message.add_filter("templates", "enable", "1")
	message.add_filter("templates", "template_id", CONFIG["SENDGRID_ACCOUNT_CONFIRM_TEMPLATE"])
	message.add_substitution("token", token)	

	status, msg = sg.send(message)


