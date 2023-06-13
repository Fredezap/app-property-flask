from wtforms import Form
from wtforms import BooleanField, SubmitField, StringField, PasswordField, validators
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length

class End_paymant_form(Form):
	ID = DataRequired("ID")
	cbu = StringField("searched")
	amount = StringField("amit")
	detail = StringField("asd")
	amount = SubmitField("Submit")

class EditForm(Form):
	searched = StringField("searched")
	submit = SubmitField("Submit")