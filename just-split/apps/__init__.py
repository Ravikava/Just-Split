from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

from logging.config import dictConfig

import os,logging


app = Flask(__name__,template_folder=os.getcwd() + '/apps/templates')
app.config.from_object('config.config')

app.wsgi_app = DispatcherMiddleware(NotFound(), {'/api': app.wsgi_app})

# dictConfig(app.config['LOGGING'])
# logger = logging.getLogger()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_timeout': 1800,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

jwt = JWTManager(app)


# from apps.helpers.send_mail import send_email
# @app.route('/health-check/')
# def hello_():
#     """
#     Add health check route
#     """
#     send_email()
#     return jsonify({
#         'Message': 'Done ... Congratulation'
#     })
from apps.database import models
from apps.api.user import routes
from apps.api.friends import routes