# -*- coding: UTF-8 -*-
# coding:utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, HiddenField 
from wtforms import validators
from models import User
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
	email = StringField(u'Email', [validators.Required()])
	password = PasswordField(u'Password', [validators.Required()])
	submit = SubmitField('Sign Up')
	class Meta():
		__model__ = 'User'