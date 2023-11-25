from flask import Flask
from os import getenv

from app.config import Config

from dotenv import load_dotenv

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.config['SECRET KEY'] = getenv('SECRET_KEY')

  from .routes.home import home
  from .routes.userprofile import userprofile
  
  app.register_blueprint(home,url_prefix='/')
  app.register_blueprint(userprofile, url_prefix='/userprofile')

  return app