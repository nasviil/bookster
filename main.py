from app import create_app
from dotenv import load_dotenv
import cloudinary

load_dotenv()

app = create_app()

# Configure Cloudinary
def configure_cloudinary():
    cloudinary.config(
        cloud_name="dclxaugvd",
        api_key="412149475729753",
        api_secret="VJNHyUvJEUXrrH2uAmfQDhIUIRk"
    )

if __name__ == '__main__':
  app.run(debug=True)
