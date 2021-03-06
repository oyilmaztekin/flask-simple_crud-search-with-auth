# -*- coding: UTF-8 -*-
# coding:utf-8
from flask import Flask, request
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
import sys
from flask.ext.security import Security
from flask_debugtoolbar import DebugToolbarExtension
from flask_humanize import Humanize

reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask(__name__)
humanize = Humanize(app)

#normal hali
app.config["MONGODB_SETTINGS"] = {
'DB': "copylighter",
'host':'mongodb://localhost/copylighter',
'username':'copyOz',
'port':27017,
'password':'7e0522bfd98d2051a20a0aca5fb3899f'
}

#AŞAĞIDAKİ KISIM HEROKU İÇİN HAZIRLANDI

#app.config["MONGODB_SETTINGS"] = {
#'DB': "heroku_9d72c5vb",
#'host':'ds037145.mongolab.com:37145/heroku_9d72c5vb',
#'username':'copyOz',
#'password':'7e0522bfd98d2051a20a0aca5fb3899f'
#}

app.config["SECRET_KEY"] = '6cf34ed05e241ac72456425779220bfeaf3557ef8371bed4'

#app.config["DEBUG"] = True
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SESSION_COOKIE_SECURE'] = True

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

db = MongoEngine(app)
app.config['SECURITY_RECOVERABLE'] = True
app.session_interface = MongoEngineSessionInterface(db)

toolbar = DebugToolbarExtension(app)
#import admin


if __name__ == "__main__":
	app.run(debug=True)

import models
import views
