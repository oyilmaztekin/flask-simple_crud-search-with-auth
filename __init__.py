# -*- coding: UTF-8 -*-
# coding:utf-8
from flask import Flask
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
import sys
from flask.ext.security import Security

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "copylighter"}
app.config["SECRET_KEY"] = '6cf34ed05e241ac72456425779220bfeaf3557ef8371bed4'
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
SECURITY_RECOVERABLE = True
db = MongoEngine(app)
app.config['SECURITY_RECOVERABLE'] = True
app.session_interface = MongoEngineSessionInterface(db)

if __name__ == "__main__":
	app.run(debug=True)

import models
import views

