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

	# if not currseUlr.rsvp:
	# 	attending = "Undecided"
	# else:
	# 	attending = currUser.attending

	checked_in = False
	if "checked_in" in currUser:
		checked_in = currUser.checked_in
	user = User(currUser.id, currUser.email, currUser.first_name, currUser.last_name, currUser.type_account) 
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

def add_hacker(fields, email, password):
	existingUser = get_user(email)
	if existingUser is not None:
		raise UserExistsError

	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # application_fields = ["firstname", "lastname", "school", "age", "grade", "gender", "free_response1", "link1", "link2", "link3", "dietary_restrictions", "t_shirt_size", "parent1_name", "parent1_home_num", "parent1_cell_num", "parent1_email", "parent2_name", "parent2_home_num", "parent2_cell_num", "parent2_email", "school_street", "school_town", "school_state", "school_phone_num", "school_principal_name", "school_principal_email", "cs_teacher_name", "cs_teacher_email",  "mlh_terms", "mlh_coc"]
    
	new_entry = UserEntry(type_account = "hacker", email = email, hashed = hashed, first_name = fields['first_name'], last_name = fields['last_name'], school = fields['school'], gender = fields['gender'], beginner = fields['beginner'], ethnicity = fields['ethnicity'], grade = fields['grade'], age = fields['age'], num_hackathons = fields['num_hackathons'], free_response1 = fields['free_response1'], link1 = fields['link1'], link2 = fields['link2'], link3 = fields['link3'], t_shirt_size = fields['t_shirt_size'], dietary_restrictions = fields['dietary_restrictions'], parent1_name = fields['parent1_name'], parent1_home_num = fields['parent1_home_num'], parent1_cell_num = fields['parent1_cell_num'], parent1_email = fields['parent1_email'], parent2_name = fields['parent2_name'], parent2_home_num = fields['parent2_home_num'], parent2_cell_num = fields['parent2_cell_num'], parent2_email = fields['parent2_email'], school_street = fields['school_street'], school_town = fields['school_town'], school_state = fields['school_state'], school_phone_num = fields['school_phone_num'], school_principal_name = fields['school_principal_name'], school_principal_email = fields['school_principal_email'], cs_teacher_name = fields['cs_teacher_name'], cs_teacher_email = fields['cs_teacher_email'], mlh_coc = fields['mlh_coc'], mlh_terms = fields['mlh_terms'])
	new_entry.save()
	validate_email(email)


def add_mentor(fields, email, password):
	existingUser = get_user(email)
	if existingUser is not None:
		raise UserExistsError
	
	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

	new_entry = UserEntry(type_account = "mentor", email = email, hashed = hashed, first_name = fields['first_name'], last_name = fields['last_name'], school = fields['school'], phone = fields['phone'], num_hackathons = fields['num_hackathons'], mentor_free_response1 = fields['mentor_free_response1'], mentor_free_response2 = fields['mentor_free_response2'], github_link = fields['github_link'], linkedin_link = fields['linkedin_link'], site_link = fields['site_link'], other_link = fields['other_link'], mlh_coc = fields['mlh_coc'], mlh_terms = fields['mlh_terms'])
	new_entry.save()
	
	validate_email(email)

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

