from flask import Flask
from flask_mail import Mail
from os import getenv
from flask_mysql_connector import MySQL
from flask_login import LoginManager
import cloudinary
import cloudinary.uploader
import cloudinary.api

from app.config import Config

from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()
mail = Mail()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  mysql.init_app(app)
  app.config['SECRET_KEY'] = getenv('SECRET_KEY')
  app.config['SESSION_TYPE'] = 'filesystem'

  app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
  app.config['MAIL_PORT'] = 2525
  app.config['MAIL_USERNAME'] = '6ce1972ec0658c'
  app.config['MAIL_PASSWORD'] = '1d5ad759a5426d'
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USE_SSL'] = False
  app.config['MAIL_DEBUG'] = True
  app.config['MAIL_DEFAULT_SENDER'] = 'bookster@gmail.com'


  mail.init_app(app)

  # cloudinary.config(
  #   CLOUD_NAME=getenv('CLOUD_NAME'),
  #   API_KEY=getenv('API_KEY'),
  #   API_SECRET=getenv('API_SECRET')
  # )

  from .routes.home import home
  from .routes.auth import auth

  app.register_blueprint(home,url_prefix='/')
  app.register_blueprint(auth,url_prefix='/')

  from .models.models import User

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
      return User(user_id)

  return app