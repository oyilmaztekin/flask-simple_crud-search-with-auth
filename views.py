# -*- coding: UTF-8 -*-
# coding:utf-8
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, login_user, logout_user
from copylighter import db, app, login_manager
import datetime
from models import Note, User
from forms import LoginForm, SignUpForm, NoteForm, SearchForm, deleteQuoteForm
from flask_login import UserMixin
import hashlib, uuid
from slugify import slugify
from mongoengine.errors import NotUniqueError, ValidationError
import re
from flask.ext.login import current_user
from collections import Counter
from pymongo.errors import OperationFailure
from passlib.hash import sha256_crypt
#import logging loglamayı bununla yapabilirsin.
import logging
#from flask.ext.mongoengine import mongoengine



username = ""
Email_Regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

URl_Regex = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

password_hash = ""

#index ten register yapılabiliyor.
@app.route("/index", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('profile')+('/'+current_user.slug))
	else:

		formS = SignUpForm()

		if request.method == 'POST':
			formS = SignUpForm(request.form)

			if formS.validate() == False:
				flash('Something went wrong','danger')
				return render_template('index.html', form=formS)

			if formS.validate_on_submit():
				password = formS.password.data
				password_hash = sha256_crypt.encrypt(password)
				form_email = formS.email.data

				if not Email_Regex.match(form_email):
					flash('Invalid email adress','danger')
					return render_template("index.html", form=formS, title="Copylighter", regex="Invalid email adress")


				newuser = User(name=formS.name.data, email=formS.email.data, password=password_hash)
				try:
					newuser.save()

				except NotUniqueError:
					flash('Username or email already exists','danger')
					return render_template("index.html", form=formS, title="Copylighter")

				flash('Successfully registered. You can login now','success')
				return redirect(url_for('login'))
				

		return render_template("index.html", form=formS, title="Copylighter")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
	return render_template("500.html"), 500


@app.route("/profile",methods=['GET','POST'])
@app.route("/profile/<slug>",methods=['GET','POST'])
@login_required
def profile(slug):
	#variables
	form = NoteForm()

	if request.method == 'POST':
		try:
			form = NoteForm(request.form)

			if form.validate() == False:
				flash("Something went wrong.",'danger')
				return render_template('profile.html', form=form, search_form=SearchForm(), delete_quote=deleteQuoteForm())

			if form.validate_on_submit():
				form_urlLink = form.URLLink.data
				
				if form.URLLink.data != '':
					if not URl_Regex.match(form_urlLink):
						flash('Invalid URL adress','danger')
						return render_template("profile.html", form=form, search_form=SearchForm(), regex="Invalid URL adress", delete_quote=deleteQuoteForm())

				tags = form.tags.data
				tagList = tags.split(",")
				
				note = Note(content=form.content.data, tags=tagList, URLLink=form.URLLink.data)
				note.save()

				current_user.notes.append(note)
				current_user.save()

				flash('Quote saved successfully.','success')
				return render_template('profile.html', form=form, search_form=SearchForm(), delete_quote=deleteQuoteForm())
				
		except ValidationError:
			flash('UPPPS! Tags or Url was wrong','danger')
			return render_template('profile.html', form=form, search_form=SearchForm(), delete_quote=deleteQuoteForm())

	return render_template("profile.html", title=current_user.name+"'s Quotes", form=form, search_form=SearchForm(), delete_quote=deleteQuoteForm())


@app.route("/search" ,methods=['POST'])
@login_required
def search():
	searchForm = SearchForm(request.form)

	if request.method == 'POST':
		searchForm = SearchForm(request.form)
		searchedby = searchForm.search.data

		if searchForm.validate() == False:
			flash("Empty search.",'warning')
			userNote = Note.objects.search_text(searchForm.search.data).as_pymongo()

		if searchForm.validate_on_submit():
			#noteResult = Note.objects.search_text(content=SearchForm.search.data).first()
			try:
				userNote = Note.objects.search_text(searchForm.search.data).as_pymongo()
			except OperationFailure:
				flash("sometihng went wrong","danger")
				render_template("search.html", title=searchedby, delete_quote=deleteQuoteForm(), search_form=searchForm, result=userNote)
			#document = notes.objects(content=searchForm.search.data).first()
			#print userNote

	return render_template("search.html", title=searchedby, search_form=searchForm, delete_quote=deleteQuoteForm(), result=userNote)


@app.route("/delete_quote/<string:id>" ,methods=['POST'])
@login_required
def delete_quote(id):
	note = Note.objects(id=id).first()

	deleteNote = deleteQuoteForm()
	if request.method == 'POST':
		deleteNote =deleteQuoteForm(request.form)

		if deleteNote.validate == False:
			flash('Faliure','danger')
			return redirect(url_for('profile')+('/'+current_user.slug))

		if deleteNote.validate_on_submit():
			note = Note.objects(id=id).first()

			current_user.notes.remove(note)
			current_user.save()

			note.delete()

			flash('Successfully deleted','warning')


	return render_template("delete.html", title="delete", delete_note=deleteNote, note=note )

@login_manager.user_loader
def load_user(id):
    return User.objects.get(id=id)
    try:
    	pass
    except DoesNotExist:
    	logging.warning("user does not exist")

@app.route("/login", methods=['GET','POST'])
def login():

	if current_user.is_authenticated:
		flash("You're already registered", "info")
		return redirect(url_for('profile')+('/'+current_user.slug))

	form = LoginForm()
	

	if request.method == 'POST':
		form = LoginForm()
		passW = form.password.data

		if form.validate_on_submit():
			user = User.objects(email=form.email.data).first()

			if not Email_Regex.match(form.email.data):
				flash('Invalid email adress','danger')
				return render_template("login.html", form=form, title="Copylighter", regex="Invalid email adress")


			if user is not None: 
				if sha256_crypt.verify(passW, user.password):
					#login_user(user, form.remember_me.data)
					login_user(user)
					slug = slugify(user.name)

					flash('We are glad you came {}.'.format(user.name),'success')
					return redirect(request.args.get('next') or url_for('profile', slug=slug))
				
				else:
					flash('Password does not match with the email','danger')
					return render_template("login.html", form=form, title="Cp-Login", regexpassword="Wrong Password")	

			else:
				flash('There is no email such as.  '+form.email.data,'danger')
				return render_template("login.html", form=form, title="Cp-Login", regex="Email does not found")
		else:
			flash("Informations doesn't entered requirely","danger")
			return render_template("login.html", form=form, title="cp-login")
	return render_template("login.html", form=form, title="Cp-Login")

@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	session.clear()
	flash('Logged out','info')
	return redirect(url_for('index'))

#bu kısım eğer kaydol sayfasına özel olarak ziyaret edilmesi gerekirse - google vs...
@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		flash("You're already registered", "info")
		return redirect(url_for('profile')+('/'+current_user.slug))
	formS = SignUpForm()

	if request.method == 'POST':
		formS = SignUpForm()

		if formS.validate() == False:
			flash('Something went wrong','danger')
			return render_template('register.html', form=formS)

		if formS.validate_on_submit():
			password = formS.password.data
			password_hash = sha256_crypt.encrypt(password)

			form_email = formS.email.data
			
			if not Email_Regex.match(form_email):
				flash('Invalid email adress','danger')
				return render_template("register.html", form=formS, title="Copylighter", regex="Invalid email adress")

			newuser = User(name=formS.name.data, email=formS.email.data, password=password_hash)
			try:
				user_mail = User.objects(email=formS.email.data).first()
				if form_email == user_mail:
					print "asd"
				newuser.save()

			except NotUniqueError:
				flash('Username or email already exists','danger')
				return render_template("register.html", form=formS, title="Copylighter")
			flash('You have successfully registered. You can login now','success')
			return redirect(url_for('login'))

	return render_template("register.html", form=formS, title="Register to Copylighter")
