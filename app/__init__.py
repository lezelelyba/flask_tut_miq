import os

import flask
import flask_login
import flask_openid
import flask_sqlalchemy

import config

main = flask.Flask(__name__)
main.config.from_object('config')
db = flask_sqlalchemy.SQLAlchemy(main)

lm = flask_login.LoginManager()
lm.init_app(main)
lm.login_view = 'login'

oid = flask_openid.OpenID(main, os.path.join(config.basedir, 'tmp'))

from app import views, models
