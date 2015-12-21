# -*- coding: UTF-8 -*-
# coding:utf-8
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, login_user, logout_user
from copylighter import db, app, login_manager
import datetime
from models import Note, NoteRef, User, TagRef
from forms import LoginForm,SignUpForm, NoteForm
from flask_login import UserMixin
import hashlib, uuid
from slugify import slugify
from mongoengine.errors import NotUniqueError, ValidationError
import re
from flask.ext.login import current_user

username = ""
Email_Regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

@app.route("/index", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def index():	
	formS = SignUpForm()

	if request.method == 'POST':
		formS = SignUpForm(request.form)
		
		if formS.validate() == False:
			flash('Something went wrong','danger')
			return render_template('index.html', form=formS)

		if formS.validate_on_submit():					
			hashash = formS.password.data
			salt = uuid.uuid4().hex
			hashed_password = hashlib.sha224(hashash + salt).hexdigest()

			form_email = formS.email.data
			if not Email_Regex.match(form_email):
				flash('Invalid email adress','danger')
				return render_template("index.html", form=formS, title="Copylighter", regex="Invalid email adress")


			newuser = User(name=formS.name.data, email=formS.email.data, password=hashed_password)				
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
		form = NoteForm(request.form)
		if form.validate() == False:
			flash('Qutoe field is required','danger')
			return render_template('profile.html', form=form)
		
		if form.validate_on_submit():					
			sum_con = form.content.data[0:120]
			tags = form.tags.data
			tagList = tags.split(",")
			
			note = Note(content=form.content.data, tags=tagList, title=sum_con)		
			note.save()
			
			current_user.notes.append(note)
			current_user.save() 
			
			noteRef = NoteRef(note_id=note.id, user_id=current_user.id)
			noteRef.save()
			
			for item in tagList:
				tagRef = TagRef(tags=item, note_id=[note.id,])
				tagRef.save()

			#try:
				#note.save()
			#except ValidationError:
				#flash('Something went wrong.','danger')
				#return render_template('profile.html', form=form)
			
			flash('Quote saved successfully.','success')
			return render_template('profile.html', form=form, )

	return render_template("profile.html", title=current_user.name, form=form)


@login_manager.user_loader
def load_user(id):
    return User.objects.get(id=id)
    try:
    	pass
    except DoesNotExist:
    	print "asdasd"

@app.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm()
		if form.validate_on_submit():
			user = User.objects(email=form.email.data).first()
			if user is not None:
				login_user(user, form.remember_me.data)
				slug = slugify(user.name)
				#flash('Logged in successfully as {}.'.format(user.name),'success')
				flash('Logged in successfully','success')
				return redirect(request.args.get('next') or url_for('profile', slug=slug))
			else:
				flash('Wrong username or password.','danger')
				return render_template("login.html", form=form)
	return render_template("login.html", form=form, title="Cp-Login")

@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	session.clear()
	flash('Logged out','info')
	return redirect(url_for('index'))

@app.route("/register", methods=['GET','POST'])
def register():
	formS = SignUpForm()

	if request.method == 'POST':
		formS = SignUpForm(request.form)
		
		if formS.validate() == False:
			flash('Something went wrong','danger')
			return render_template('register.html', form=formS)

		if formS.validate_on_submit():					
			hashash = formS.password.data
			salt = uuid.uuid4().hex
			hashed_password = hashlib.sha224(hashash + salt).hexdigest()
			form_email = formS.email.data
			if not Email_Regex.match(form_email):
				flash('Invalid email adress','danger')
				return render_template("register.html", form=formS, title="Copylighter", regex="Invalid email adress")

			newuser = User(name=formS.name.data, email=formS.email.data, password=hashed_password)				
			try:
				newuser.save()
				
			except NotUniqueError:
				flash('Username or email already exists','danger')
				return render_template("register.html", form=formS, title="Copylighter")
			flash('You have successfully registered. You can login now','success')
			return redirect(url_for('login'))

	return render_template("register.html", form=formS, title="Register to Copylighter")
