from wtforms import Form, TextField, ValidationError, validators

class MailList(Form):
    email = TextField("Email", [
        validators.DataRequired(message = "Enter an email."),
        validators.Email(message = "Invalid email address.")
    ])
