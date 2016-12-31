from application import CONFIG, app
from .models import *
from flask_login import login_user, logout_user
import bcrypt
import re
import sendgrid
from sendgrid.helpers.mail import *
import time
import requests
import json
from itsdangerous import URLSafeTimedSerializer

AuthenticationError = Exception("AuthenticationError", "Invalid credentials.")
UserExistsError = Exception("UserExistsError", "Email already exists in database.")
UserDoesNotExistError = Exception("UserDoesNotExistError", "Account with given email does not exist.")
GenericMongoError = Exception("GenericMongoError")

login_manager = LoginManager()
login_manager.init_app(app)

sg = sendgrid.SendGridAPIClient(apikey=CONFIG["SENDGRID_API_KEY"])
ts = URLSafeTimedSerializer(CONFIG["SECRET_KEY"])

@login_manager.user_loader
def load_user(user_id):	
	try:
		user_entries = UserEntry.objects(id = user_id)
		if user_entries.count() != 1:
			return None
		currUser = user_entries[0]
	except Exception:
		raise GenericMongoError

	# if not currUser.rsvp:
	# 	attending = "Undecided"
	# else:
	# 	attending = currUser.attending

	checked_in = False
	if "checked_in" in currUser:
		checked_in = currUser.checked_in
	user = User(currUser.id, currUser.email, currUser.firstname, currUser.lastname, currUser.type_account) 
	return user

def get_user(email):
	try:
		entries = UserEntry.objects(email = email.lower())
		if entries.count() == 1:
			return entries[0]
		return None
	except Exception:
		raise GenericMongoError

def verify_user(email, password):
	currUser = get_user(email)
	if currUser is None:
		return None
	hashed = currUser.hashed		

	if bcrypt.hashpw(password.encode("utf-8"), hashed.encode("utf-8")) == hashed.encode("utf-8"):
		return load_user(currUser.id)
	else:
		return None

def login(email):
	user = load_user(get_user(email).id)
	if user != None:
		login_user(user)
	else:
		raise UserDoesNotExistError

def logout():
	logout_user()

def add_hacker(email, firstname, lastname, password, school, gender, beginner, ethnicity, grade, num_hackathons, link1, link2, link3, t_shirt_size, free_response1, food_allergies, mlh_terms, type_account):
	existingUser = get_user(email)
	if existingUser is not None:
		raise UserExistsError
	
	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
	new_entry = UserEntry(email = email.lower(), hashed = hashed, firstname = firstname, lastname = lastname, type_account = type_account, school = school, gender = gender, beginner = beginner, ethnicity = ethnicity, grade = grade, num_hackathons = num_hackathons, link1 = link1, link2 = link2, link3 = link3, t_shirt_size = t_shirt_size, free_response1 = free_response1, food_allergies = food_allergies, mlh_terms = mlh_terms)
	new_entry.save()
	
	validate_email(email)

####### uncomment/fix below once mentor criteria is added

# def add_mentor(#######):
# 	existingUser = get_user(email)
# 	if existingUser is not None:
# 		raise UserExistsError
	
# 	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
# 	new_entry = UserEntry(##########)
# 	new_entry.save()
	
# 	validate_email(email)

def tokenize_email(email):
	return ts.dumps(email, salt = CONFIG["EMAIL_TOKENIZER_SALT"])

def detokenize_email(token):
	return ts.loads(token, salt = CONFIG["EMAIL_TOKENIZER_SALT"], max_age = 86400 * 60)

def send_recovery_email(email):
	user = get_user(email)

	if user is None:
		raise UserDoesNotExistError

	token = tokenize_email(email)
	from_email = Email("contact@hackbca.com")
	to_email = Email(email)
	subject = "hackBCA IV - Account Recovery"
	content = Content("text/html", "<p></p>")
	mail = Mail(from_email, subject, to_email, content)
	mail.template_id = CONFIG["SENDGRID_ACCOUNT_RECOVERY_TEMPLATE"]
	mail.personalizations[0].add_substitution(Substitution("%prefix%", "www")) 
	mail.personalizations[0].add_substitution(Substitution("%token%", token)) 
	response = sg.client.mail.send.post(request_body=mail.get())

def change_name(email, firstname, lastname):
	account = get_user(email)

	if account is None:
		raise UserDoesNotExistError

	account.firstname = firstname
	account.lastname = lastname
	account.save()

	login(email) #To update navbar

def change_password(email, password):
	account = get_user(email)

	if account is None:
		raise UserDoesNotExistError

	hashed = str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()))[2:-1]
	account.hashed = hashed
	account.save()

# def change_account_type(email, account_type):
# 	account = get_user(email)

# 	if account.type_account == account_type:
# 		return
# 	account.type_account = account_type

# 	clear_application(account.email)

# 	account.save()

# 	login(email)

def delete_account(email):
	account = get_user(email)
	account.delete()
	

def validate_email(email):
	token = tokenize_email(email)
	from_email = Email("contact@hackbca.com")
	to_email = Email(email)
	subject = "hackBCA IV - Registration Confirmation"
	content = Content("text/html", "<p></p>")
	mail = Mail(from_email, subject, to_email, content)
	mail.template_id = CONFIG["SENDGRID_ACCOUNT_CONFIRM_TEMPLATE"]
	mail.personalizations[0].add_substitution(Substitution("%token%", token)) 
	response = sg.client.mail.send.post(request_body=mail.get())

def confirm_email(token):
	email = detokenize_email(token)
	try:
		entry = UserEntry.objects(email = email.lower())[0]
		entry.confirmed = True
		entry.save()
	except Exception:
		raise GenericMongoError

def get_user_attr(email, attr):
	user = get_user(email)
	if user is None:
		raise UserDoesNotExistError
	
	return getattr(user, attr)

def set_user_attr(email, attr, value):
	user = get_user(email)
	if user is None:
		raise UserDoesNotExistError
	
	setattr(user, attr, value)

	user.save()

def clear_application(email):
	user = get_user(email)

	if user is None:
		raise UserDoesNotExistError
	for key in application_fields:
		setattr(user, key, None)

	user.save()

def get_application(email):
	user = get_user(email)
	if user is None:
		raise UserDoesNotExistError
	app = {}
	for key in application_fields:
		if getattr(user, key) is not None:
			app[key] = getattr(user, key)
	return app

def save_form_data(email, app):
	user = get_user(email)
	
	if user is None:
		raise UserDoesNotExistError
	for key in app:		
		if key == "save" or key == "submit":
			continue
		setattr(user, key, app[key])

	user.save()

def accept_applicant(uid):
	if CONFIG["DEBUG"]:
		url = 'http://localhost:5000/api/accept_applicant'
	else:
		url = 'http://staff.hackbca.com/api/accept_applicant'
	data = {'secret-key' : CONFIG["SECRET_KEY"], 'user-id': uid}
	headers = {'Content-Type': 'application/json'}

	r = requests.post(url, data=json.dumps(data), headers=headers)

