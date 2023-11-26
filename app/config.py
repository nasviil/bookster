from os import getenv

from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY = getenv('SECRET_KEY')
    CLOUD_NAME = getenv("CLOUD_NAME")
    API_KEY = getenv("API_KEY")
    API_SECRET = getenv("API_SECRET")