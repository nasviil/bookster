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
  app.config['SECRET KEY'] = getenv('SECRET_KEY')

  from app.routes.home import home_bp
  from .routes.auth import auth
  from .routes.userprofile import userprofile
  

  app.register_blueprint(home_bp,url_prefix='/')
  app.register_blueprint(auth,url_prefix='/')
  app.register_blueprint(userprofile, url_prefix='/')

  from .models.models import User

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)


  @login_manager.user_loader
  def load_user(username):
      return User(username)

  return app

