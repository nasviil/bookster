from flask import Flask
from os import getenv
from flask_mysql_connector import MySQL
from flask_login import LoginManager
from app.routes.home import home
from .routes.auth import auth
from .routes.userprofile import userprofile
from app.config import Config
from .models.models import User
from cloudinary import config as cloudinary_config



from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'

    # Cloudinary setup
    cloudinary_config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
        
    )

    # Register Blueprints
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(userprofile, url_prefix='/')

    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        return User(username)

    return app
