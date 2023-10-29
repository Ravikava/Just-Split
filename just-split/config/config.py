import os,logging,datetime
from dotenv import load_dotenv

from flask_mail import Mail

from apps import app
# Get the .env variables
load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_TOKEN_LOCATION = ['headers']
JWT_IDENTITY_CLAIM = 'user_id'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)