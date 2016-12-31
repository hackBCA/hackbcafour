
from wtforms import Form, TextField, PasswordField, SelectField, TextAreaField, BooleanField, validators, ValidationError, RadioField
import re


gender_choices = [
    ("", "Gender"),
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
    ("rns", "Rather Not Say")
]

beginner_choices = [
    ("", "Are you a beginner?"),
    ("yes", "Yes"),
    ("no", "No")
]


ethnicity_choices = [
    ("", "Ethnicity"),
    ("white", "White"),
    ("african_american", "African American"),
    ("asian_pacific", "Asian or Pacific Islander"),
    ("american_indian_alaskan_native", "American Indian or Alaskan Native"),
    ("multiracial", "Multiracial"),
    ("hispanic", "Hispanic origin"),
    ("other", "Other"),
    ("rns", "Rather Not Say")
]

num_hackathons_choices = [
    ("", "How many hackathons have you been to?"),
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5+")
]

grade_choices = [
    ("", "What grade are you in?"),
    ("9", "9th"),
    ("10", "10th"),
    ("11", "11th"),
    ("12", "12th")
]

shirt_sizes = [
    ("", "What is your shirt size?"),
    ("XS", "Extra Small"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large")
]

type_account_choices = [
    ("hacker", "Hacker"),
    ("mentor", "Mentor")
]


free_response1_prompt = "Why do you want to come to hackBCA?"


class HackerRegistrationForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address.")
    ], description = "Email")
    first_name = TextField("First Name", [
        validators.Required(message = "You must enter a first name.")
    ], description = "First Name")
    last_name = TextField("Last Name", [
        validators.Required(message = "You must enter a last name.")
    ], description = "Last Name")

    school = TextField("School Name", [
        validators.Required(message = "Enter your school's name.")
    ], description = "School Name")

    gender = SelectField("Gender", [validators.Required(message = "You must select an option.")], choices = gender_choices, description = "Gender")
    other_gender = TextField("Other Gender", description = "Other Gender")
    beginner = SelectField("Are you a beginner?", [validators.Required(message = "You must select an option.")], choices = beginner_choices, description = "Are you a beginner?")
    ethnicity = SelectField("Ethnicity", [validators.Required(message = "You must select an option.")], choices = ethnicity_choices, description = "Ethnicity")
    grade = SelectField("Grade", [validators.Required(message = "You must select an option.")], choices = grade_choices, description = "Grade")
    num_hackathons = SelectField("How many hackathons have you attended?", [validators.Required(message = "You must select an option.")], choices = num_hackathons_choices, description = "How many hackathons have you attended?")

    link1 = TextField("Link #1", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], description = "Link #1 (Optional)")
    link2 = TextField("Link #2", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], description = "Link #2 (Optional)")
    link3 = TextField("Link #3", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], description = "Link #3 (Optional)")
    
    t_shirt_size = SelectField("What is your shirt size?", [validators.Required(message = "You must select an option.")], choices = shirt_sizes, description = "What is your shirt size?")

    free_response1 = TextAreaField(free_response1_prompt, [
        validators.Required(message = "You must answer this question."),
        validators.Length(max = 500, message = "Response must be less than 500 characters long.")
    ], description = "250 words maximum.")

    food_allergies = TextAreaField("Allergies", [
        validators.optional(),
    ], description = "Do you have any allergies?")


    mlh_terms = BooleanField("I agree", [
        validators.Required(message = "Please read and agree to the MLH Code of Conduct.")
        ], description = "I agree to the MLH Code of Conduct.", default = False)
    password = PasswordField("Password", [
        validators.Required(message = "You must enter a password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], description = "Password")
    confirm_password = PasswordField("Confirm Password", description = "Confirm Password")

    def validate_confirm_password(form, field):
        password = form['password'].data
        if len(password) >= 8 and password != field.data:
            raise ValidationError("Passwords must match.")
    def validate(self): #Man I love validators.URL
        links = ["link1", "link2", "link3"]
        originalValues = {}

        for link in links: #Temporarily prefix all links with http:// if they are missing it
            attr = getattr(self, link)
            val = attr.data
            originalValues[link] = val
            if re.match("^(http|https)://", val) is None:
                val = "http://" + val
            attr.data = val
            setattr(self, link, attr)

        rv = Form.validate(self)

        for link in links: #Revert link values back to actual values
            attr = getattr(self, link)
            attr.data = originalValues[link]
            setattr(self, link, attr)

        if not rv:
            return False
        return True

    def validate_other_gender(form, field):
        if form['gender'].data == 'other' and field.data == "":
            raise ValidationError("Enter your gender.")

class RegistrationForm(Form):
    type_account = SelectField("Account Type", [validators.Required(message = "You must select an option.")], choices = type_account_choices, description = "Choose account type.")

class LoginForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], description = "Email")
    password = PasswordField("Password", [], description = "Password")

class EmailForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], description = "Email")

class RecoverForm(Form):
    password = PasswordField("Password", [
        validators.Required(message = "You must enter a password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], description = "Password")
    confirm_password = PasswordField("Confirm Password", description = "Confirm Password")

    def validate_confirm_password(form, field):
        password = form['password'].data
        if len(password) >= 8 and password != field.data:
            raise ValidationError("Passwords must match.")

class ChangeNameForm(Form):
    firstname = TextField("First Name", [
        validators.Required(message = "You must enter a first name.")
    ], description = "First Name")
    lastname = TextField("Last Name", [
        validators.Required(message = "You must enter a last name.")
    ], description = "Last Name")

class ChangePasswordForm(Form):
    password = PasswordField("Password", [
        validators.Required(message = "You must enter your current password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], description = "Password")

    new_password = PasswordField("New Password", [
        validators.Required(message = "You must choose a new password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], description = "New Password")
    confirm_password = PasswordField("Confirm New Password", description = "Confirm New Password")

    def validate_confirm_password(form, field):
        password = form['new_password'].data
        if len(password) >= 8 and password != field.data:
            raise ValidationError("Passwords must match.")



  

    
