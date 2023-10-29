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

  app.register_blueprint(home,url_prefix='/')

  return app