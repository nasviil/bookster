from app import create_app
from os import getenv

from app.config import Config

from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
  app.secret_key = getenv('SECRET_KEY')
  app.run(debug=True)