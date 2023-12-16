from flask import Flask
from flask_mail import Mail
from os import getenv
from flask_mysql_connector import MySQL
from flask_login import LoginManager
from cloudinary import config as cloudinary_config
from dotenv import load_dotenv
from app.config import Config
from app.models.models import User

from dotenv import load_dotenv


load_dotenv()

mysql = MySQL()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    mail.init_app(app)
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


    # Cloudinary setup
    cloudinary_config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    from app.routes.home import home
    from app.routes.auth import auth
    from app.routes.userprofile import userprofile

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





