from wtforms import Form, TextField, PasswordField, SelectField, TextAreaField, BooleanField, validators, ValidationError, RadioField
import re


phone_regex = "(\+\d+-?)?((\(?\d{3}\)?)|(\d{3}))-?\d{3}-?\d{4}$"

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

num_hackathons_choices_mentor = [
    ("", "How many hackathons have you mentored at?"),
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

free_response1_prompt_mentor = "Please list languages/frameworks/technologies that you would like to mentor students in."
free_response2_prompt_mentor = "Would you like to run a workshop? If so, please briefly describe your ideas."


class HackerRegistrationForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address.")
    ], render_kw={"class": 'text'}, description = "Email")
    first_name = TextField("First Name", [
        validators.Required(message = "You must enter a first name.")
    ], render_kw={"class": 'text'}, description = "First Name")
    last_name = TextField("Last Name", [
        validators.Required(message = "You must enter a last name.")
    ], render_kw={"class": 'text'}, description = "Last Name")

    school = TextField("School Name", [
        validators.Required(message = "Enter your school's name.")
    ], render_kw={"class": 'text'}, description = "School Name")

    gender = SelectField("Gender", [validators.Required(message = "You must select an option.")], choices = gender_choices, render_kw={"class": 'text'}, description = "Gender")
    beginner = SelectField("Are you a beginner?", [validators.Required(message = "You must select an option.")], choices = beginner_choices, render_kw={"class": 'text'}, description = "Are you a beginner?")
    ethnicity = SelectField("Ethnicity", [validators.Required(message = "You must select an option.")], choices = ethnicity_choices, render_kw={"class": 'text'}, description = "Ethnicity")
    grade = SelectField("Grade", [validators.Required(message = "You must select an option.")], choices = grade_choices, render_kw={"class": 'text'}, description = "Grade")
    age = TextField("Age", [
        validators.Required(message = "Enter your age")
    ], render_kw={"class": 'text'}, description = "Age")
    num_hackathons = SelectField("How many hackathons have you attended?", [validators.Required(message = "You must select an option.")], choices = num_hackathons_choices, render_kw={"class": 'text'}, description = "How many hackathons have you attended?")

    free_response1 = TextAreaField(free_response1_prompt, [
        validators.Required(message = "You must answer this question."),
        validators.Length(max = 500, message = "Response must be less than 500 characters long.")
    ], render_kw={"class": 'text'}, description = "250 words maximum.")

    link1 = TextField("Link #1", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "Link #1 (Optional)")
    link2 = TextField("Link #2", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "Link #2 (Optional)")
    link3 = TextField("Link #3", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "Link #3 (Optional)")
    
    password = PasswordField("Password", [
        validators.Required(message = "You must enter a password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], render_kw={"class": 'text'}, description = "Password")
    confirm_password = PasswordField("Confirm Password", render_kw={"class": 'text'}, description = "Confirm Password")

    mlh_coc = BooleanField("I agree", [
    validators.Required(message = "Please read and agree to the MLH Code of Conduct.")
    ], description = "I have read & agree to the MLH Code of Conduct.", default = False)

    mlh_terms = BooleanField("I agree", [
        validators.Required(message = "Please read and agree to the MLH Terms and Conditions.")
        ], description = "I agree to the MLH Contest Terms and Conditions and the MLH Privacy Policy.", default = False)

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

class MentorRegistrationForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address.")
    ], render_kw={"class": 'text'}, description = "Email")

    first_name = TextField("First Name", [
        validators.Required(message = "You must enter a first name.")
    ], render_kw={"class": 'text'}, description = "First Name")
    
    last_name = TextField("Last Name", [
        validators.Required(message = "You must enter a last name.")
    ], render_kw={"class": 'text'}, description = "Last Name")

    school = TextField("Company/School Name", [
        validators.Required(message = "Enter your company/schools's name.")
    ], render_kw={"class": 'text'}, description = "Company/School Name")

    phone = TextField("Phone Number", [
        validators.Required(message = "Enter your preferred contact number."),
        validators.Regexp(phone_regex, message = "Please enter a valid phone number.")
    ], render_kw={"class": 'text'}, description = "Phone Number")

    num_hackathons = SelectField("How many hackathons have you mentored at?", [validators.Required(message = "You must select an option.")], choices = num_hackathons_choices_mentor, render_kw={"class": 'text'}, description = "How many hackathons have you mentored at?")

    mentor_free_response1 = TextAreaField(free_response1_prompt_mentor, [
        validators.Length(max = 500, message = "Response must be less than 500 characters long.")
    ], render_kw={"class": 'text'}, description = "500 character maximum.")

    mentor_free_response2 = TextAreaField(free_response2_prompt_mentor, [
        validators.Length(max = 500, message = "Response must be less than 500 characters long.")
    ], render_kw={"class": 'text'}, description = "500 character maximum.")
    
    github_link = TextField("Github Link", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "Github Link (Optional)")

    linkedin_link = TextField("LinkedIn", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "LinkedIn Link (Optional)")

    site_link = TextField("Personal Site", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "Personal Site Link (Optional)")

    other_link = TextField("other", [
        validators.optional(),
        validators.URL(message = "Invalid URL.")
    ], render_kw={"class": 'text'}, description = "Other Link (Optional)")
 
    password = PasswordField("Password", [
        validators.Required(message = "You must enter a password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], render_kw={"class": 'text'}, description = "Password")
    confirm_password = PasswordField("Confirm Password", render_kw={"class": 'text'}, description = "Confirm Password")

    mlh_coc = BooleanField("I agree", [
    validators.Required(message = "Please read and agree to the MLH Code of Conduct.")
    ], description = "I have read & agree to the MLH Code of Conduct.", default = False)

    mlh_terms = BooleanField("I agree", [
        validators.Required(message = "Please read and agree to the MLH Terms and Conditions.")
        ], description = "I agree to the MLH Contest Terms and Conditions and the MLH Privacy Policy.", default = False)


    def validate(self):
        links = ["github_link", "linkedin_link", "site_link", "other_link"]
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


class LoginForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], render_kw={"class": 'text'},description = "Email")
    password = PasswordField("Password", [], render_kw={"class": 'text'}, description = "Password")

class EmailForm(Form):
    email = TextField("Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], render_kw={"class": 'text'}, description = "Email")


class ApplicantInformation(Form):
    t_shirt_size = SelectField("What is your shirt size?", [validators.Required(message = "You must select an option.")], choices = shirt_sizes, description = "What is your shirt size?")

    dietary_restrictions = TextAreaField("Dietary Restrictions", [
        validators.optional(),
    ], description = "Do you have any dietary restrictions?")

    parent1_name = TextField("Parent1 Name", [
        validators.Required(message = "You must enter a first name.")
    ], description = "Parent1 Name")

    parent1_home_num = TextField("Parent1 Home Num", [
        validators.Required(message = "Enter parent 1's home number."),
        validators.Regexp(phone_regex, message = "Please enter a valid phone number.")
    ], description = "Parent1 Home Num")

    parent1_cell_num = TextField("Parent1 Cell Num", [
        validators.Required(message = "Enter parent 1's home number."),
        validators.Regexp(phone_regex, message = "Please enter a valid phone number.")
    ], description = "Parent1 Cell Num")

    parent1_email = TextField("Parent1 Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], description = "Parent1 Email")

    parent2_name = TextField("Parent2 Name", [
        validators.Required(message = "You must enter a first name.")
    ], description = "Parent2 Name")

    parent2_home_num = TextField("Parent1 Home Num", [
        validators.Required(message = "Enter parent 1's home number."),
        validators.Regexp(phone_regex, message = "Please enter a valid phone number.")
    ], description = "Parent2 Home Num")

    parent2_cell_num = TextField("Parent2 Cell Num", [
        validators.Required(message = "Enter parent 1's home number."),
        validators.Regexp(phone_regex, message = "Please enter a valid phone number.")
    ], description = "Parent2 Cell Num")

    parent2_email = TextField("Parent2 Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], description = "Parent1 Email")

    school_street = TextField("School Street", [
         validators.Required(message = "Enter your school street."),
    ], description = "School Street")

    school_town = TextField("School Town", [
         validators.Required(message = "Enter your school town."),
    ], description = "School Town")

    school_state = TextField("School State", [
         validators.Required(message = "Enter your school state."),
    ], description = "School State")

    school_phone_num = TextField("School Phone Number", [
        validators.Required(message = "Enter school's home number."),
        validators.Regexp(phone_regex, message = "Please enter a valid phone number.")
    ], description = "School Phone Number")

    school_principal_name = TextField("Principal Name", [
        validators.Required(message = "You must enter a name."),
    ], description = "Principal Name")

    school_principal_email = TextField("Principal Email", [
        validators.Required(message = "Enter an email."),
        validators.Email(message = "Invalid email address."
    )], description = "Principal Email")

    cs_teacher_name = TextField("CS Teacher Name", [
        validators.optional(),
    ], description = "CS Teacher Name")

    cs_teacher_email = TextField("CS Teacher Email", [
        validators.optional(),
        validators.Email(message = "Invalid email address."
    )], description = "Email")


class RecoverForm(Form):
    password = PasswordField("Password", [
        validators.Required(message = "You must enter a password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], description = "Password")
    confirm_password = PasswordField("Confirm Password", render_kw={"class": 'text'}, description = "Confirm Password")

    def validate_confirm_password(form, field):
        password = form['password'].data
        if len(password) >= 8 and password != field.data:
            raise ValidationError("Passwords must match.")

class ChangeNameForm(Form):
    first_name = TextField("First Name", [
        validators.Required(message = "You must enter a first name.")
    ], render_kw={"class": 'text'}, description = "First Name")
    last_name = TextField("Last Name", [
        validators.Required(message = "You must enter a last name.")
    ], render_kw={"class": 'text'}, description = "Last Name")

class ChangePasswordForm(Form):
    password = PasswordField("Password", [
        validators.Required(message = "You must enter your current password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], render_kw={"class": 'text'}, description = "Current Password")

    new_password = PasswordField("New Password", [
        validators.Required(message = "You must choose a new password."),
        validators.Length(min = 8, message = "Password must be at least 8 characters.")
    ], render_kw={"class": 'text'}, description = "New Password")
    confirm_password = PasswordField("Confirm New Password", render_kw={"class": 'text'}, description = "Confirm New Password")

    def validate_confirm_password(form, field):
        password = form['new_password'].data
        if len(password) >= 8 and password != field.data:
            raise ValidationError("Passwords must match.")



  

    
