from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    MYSQL_HOST = getenv('MYSQL_HOST')
    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_PASSWORD = getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = getenv('MYSQL_DATABASE')
    CLOUDY_NAME = getenv('CLOUDY_NAME')
    CLOUDY_KEY = getenv('CLOUDY_KEY')
    CLOUDY_SECRET = getenv('CLOUDY_SECRET')
    CLOUDY_URL = getenv('CLOUDY_URL')
