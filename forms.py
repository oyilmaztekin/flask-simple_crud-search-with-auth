# -*- coding: UTF-8 -*-
# coding:utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField, TextField
from wtforms.validators import EqualTo
from wtforms import validators
from models import User, Note
import datetime
from slugify import slugify


class LoginForm(Form):
	email = StringField(u'E-Mail', [validators.Required()])
	password = PasswordField(u'Password', [validators.Required()])
	remember_me = BooleanField(u'Remember me')
	submit = SubmitField('Log in')
	class Meta():
		__model__ = 'User'

class SignUpForm(Form):
	name = StringField(u'Username', [validators.Required()])
	email = StringField(u'Email', [validators.Required()])
	password = PasswordField(u'Password', [validators.Required()])
	submit = SubmitField('Register & Start Copylighting')
	class Meta():
		__model__ = 'User'

class NoteForm(Form):
	content = TextAreaField(u'Quote', [validators.Required()])
	URLLink = TextField(u'Source')
	tags = StringField(u'Use', [validators.Required()])
	submit = SubmitField('Add This Quote')
	class Meta():
		__model__ = 'Note'

class UpdateNoteForm(Form):
	content2 = TextAreaField(u'Quote', [validators.Required()])
	URLLink2 = TextField(u'Source')
	tags2 = StringField(u'Use', [validators.Required()])
	wtf = HiddenField()
	submit2 = SubmitField('Update This Quote')
	class Meta():
		__model__ = 'Note'

class SearchForm(Form):
	search = StringField(u'Search', [validators.Required()])
	submit = SubmitField('Search')
	class Meta():
		__model__ = 'Note'

class deleteQuoteForm(Form):
	submit = SubmitField('Delete Quote')
	class Mete():
		__model__ = 'Note'
