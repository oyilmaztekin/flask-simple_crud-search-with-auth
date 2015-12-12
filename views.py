# -*- coding: UTF-8 -*-
# coding:utf-8
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user
from copylighter import db, app, login_manager
import datetime
from forms import LoginForm,SignUpForm
from flask_login import UserMixin
from models import User


@app.route("/index")
@app.route("/")
def hello():
	return render_template("index.html", title="Copylighter")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
	return render_template("500.html"), 500

@login_manager.user_loader
def load_user(_id):
	return User.objects.get(_id)

@app.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()

	
	if form.validate_on_submit():
		login_user(user)		
		user = User.objects.filter(email=form.email.data).first()

		if user is not None:
			login_user(user, form.remember_me.data)
			flash("logged in successfully as {}.".format(user.username))
			return redirect(request.args.get('next') or url_for('index'))


		flash('Incorrect username or password')
	   
	return render_template("login.html", form=form)

@app.route("/register", methods=['GET','POST'])
def register():
	formS = SignUpForm()
	"""
	roles inserti yapmalisin. Thumblelog query lerinden örnek alabilirsin
	"""

	if request.method == 'POST':
		formS = SignUpForm()
		
		if formS.validate() == False:
			return render_template('register.html', form=formS)

		if formS.validate_on_submit():
			newuser = User(name=formS.name.data, email=formS.email.data, password=formS.password.data)				
			newuser.save()
			
			return redirect(url_for('/profile'))

	return render_template("register.html", form=formS)
