from app import create_app
from os import getenv

from app.config import Config

from dotenv import load_dotenv
import cloudinary
load_dotenv()

app = create_app()

if __name__ == '__main__':
  app.secret_key = getenv('SECRET_KEY')
  app.run(debug=True)
  app.debug = True

def configure_cloudinary():
    cloudinary.config(
        cloud_name="dclxaugvd",
        api_key="412149475729753",
        api_secret="VJNHyUvJEUXrrH2uAmfQDhIUIRk"
    )