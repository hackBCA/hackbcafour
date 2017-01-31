from flask_login import LoginManager, UserMixin
from mongoengine import *

application_fields = ["email", "first_name", "last_name", "school", "gender", "beginner", "ethnicity", "grade", "age", "num_hackathons", "free_response1", "link1", "link2", "link3", "t_shirt_size", "dietary_restrictions", "parent1_name", "parent1_home_num", "parent1_cell_num", "parent1_email", "parent2_name", "parent2_home_num", "parent2_cell_num", "parent2_email", "school_street", "school_town", "school_state", "school_phone_num", "school_principal_name", "school_principal_email", "cs_teacher_name", "cs_teacher_email", "mlh_coc", "mlh_terms"]

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
	# status = StringField(default = "Not Started")


	school = StringField()
	gender = StringField()
	beginner = StringField()
	ethnicity = StringField()
	grade = StringField()
	num_hackathons = StringField()
	t_shirt_size = StringField()
	dietary_restrictions = StringField()
	
	# decision = StringField()
	# accepted_time = IntField()
	# attending = StringField()
	# rsvp = BooleanField(default = False) #Has the user submitted their rsvp form?

	age = StringField()
	link1 = StringField()
	link2 = StringField()
	link3 = StringField()

	parent1_name = StringField()
	parent1_home_num = StringField()
	parent1_cell_num = StringField()
	parent1_email = StringField()

	parent2_name = StringField()
	parent2_home_num = StringField()
	parent2_cell_num = StringField()
	parent2_email = StringField()

	school_street = StringField()
	school_town = StringField()
	school_state = StringField()
	school_phone_num = StringField()
	school_principal_name = StringField()
	school_principal_email = StringField()
	
	cs_teacher_name = StringField()
	cs_teacher_email = StringField()
	
	free_response1 = StringField() 
	
	mlh_terms = StringField()
	mlh_coc = StringField()



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