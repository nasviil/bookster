from flask import Flask
from os import getenv
from flask_mysql_connector import MySQL
from flask_login import LoginManager

from app.config import Config

from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  mysql.init_app(app)
  app.config['SECRET_KEY'] = getenv('SECRET_KEY')

  from .routes.home import home
  from .routes.auth import auth

  app.register_blueprint(home,url_prefix='/')
  app.register_blueprint(auth,url_prefix='/')

  from .models.models import User

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)


  @login_manager.user_loader
  def load_user(username):
      return User(username)

  return app