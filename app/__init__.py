from flask import Flask
from os import getenv
from flask_login import LoginManager
import cloudinary
import cloudinary.uploader
import cloudinary.api

from app.config import Config

from dotenv import load_dotenv

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.config['SECRET KEY'] = getenv('SECRET_KEY')

  cloudinary.config['CLOUD_NAME'] = getenv('CLOUD_NAME')
  cloudinary.config['API_KEY'] = getenv('API_KEY')
  cloudinary.config['API_SECRET'] = getenv('API_SECRET')
  
  # cloudinary.config(
  #       CLOUD_NAME=CLOUD_NAME,
  #       API_KEY=API_KEY,
  #       API_SECRET=API_SECRET
  #   )

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