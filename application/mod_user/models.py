from flask_login import LoginManager, UserMixin
from mongoengine import *

application_fields = ["school", "gender", "beginner", "ethnicity", "grade", "num_hackathons", "link1", "link2", "link3", "free_response1",  "mlh_terms"]


#Mongo Object
class UserEntry(Document):
	meta = {
		"strict": False
	}

	# hacker application info !!
	email = StringField(required = True)
	hashed = StringField(required = True)

	firstname = StringField(required = True)
	lastname = StringField(required = True)

	type_account = StringField(required = True, default = "hacker")
	confirmed = BooleanField(required = False, default = False)
	status = StringField(default = "Not Started")


	school = StringField()
	gender = StringField()
	beginner = StringField()
	ethnicity = StringField()
	grade = StringField()
	num_hackathons = StringField()
	t_shirt_size = StringField()
	food_allergies = StringField()
	
	# decision = StringField()
	# accepted_time = IntField()
	# attending = StringField()
	# rsvp = BooleanField(default = False) #Has the user submitted their rsvp form?


	link1 = StringField()
	link2 = StringField()
	link3 = StringField()
	
	free_response1 = StringField() 
	
	mlh_terms = StringField()



	review1 = IntField()
	reviewer1 = StringField()
	review2 = IntField()
	reviewer2 = StringField()
	review3 = IntField()
	reviewer3 = StringField()

	meta = { "strict" : False }


class User(UserMixin):
	def __init__(self, uid, email, firstname, lastname, type_account):
		#  status, decision, attending, checked_i
		self.uid = str(uid)
		self.email = email
		self.firstname = firstname
		self.lastname = lastname
		self.type_account = type_account
		# self.status = status
		# self.decision = decision
		# self.attending = attending
		# self.checked_in = checked_in

	def is_authenticated(self):
		return True

	def get_id(self):
		return self.uid

	def full_name(self):
		return self.firstname + " " + self.lastname