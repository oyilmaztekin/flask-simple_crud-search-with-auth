# -*- coding: UTF-8 -*-
# coding:utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField 
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
	tags = StringField(u'Use')
	submit = SubmitField('Add This Quote')
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




