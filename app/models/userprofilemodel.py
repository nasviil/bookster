from flask import Flask, current_app
from flaskext.mysql import MySQL
from os import getenv
from dotenv import load_dotenv  

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = getenv('MYSQL_USERNAME')
app.config['MYSQL_DATABASE_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = getenv('MYSQL_NAME')  
app.config['MYSQL_DATABASE_HOST'] = getenv('MYSQL_HOST')
mysql = MySQL(app)

class UserProfile:
    __tablename__ = 'userprofile'

    def __init__(self, user_id, name, image_url, bio, instagram, twitter, facebook):
        self.user_id = user_id
        self.name = name
        self.image_url = image_url
        self.bio = bio
        self.instagram = instagram
        self.twitter = twitter
        self.facebook = facebook
    
    @classmethod
    def get_user_profile(cls, user_id):
        print(user_id)
        select_sql = """
            SELECT *
            FROM userprofile
            WHERE user_id = %s
        """.format(cls.__tablename__)

        try:
            # Use get_db() to get a cursor and connection
            with current_app.app_context():
                connection = mysql.connect()
                cursor = connection.cursor()
                cursor.execute(select_sql, (user_id,))
                user_profile_data = cursor.fetchone()
                print(user_profile_data)

                # Check if user_profile_data is not None before iterating
                if user_profile_data is not None:
                    columns = [column[0] for column in cursor.description]
                    user_profile_data = dict(zip(columns, user_profile_data))

                    # Create an instance of UserProfile using the dictionary
                    return cls(
                        user_id=user_profile_data['user_id'],
                        name=user_profile_data['name'],
                        image_url=user_profile_data['image_url'],
                        bio=user_profile_data['bio'],
                        instagram=user_profile_data['instagram'],
                        twitter=user_profile_data['twitter'],
                        facebook=user_profile_data['facebook']
                    )
                else:
                    return None
        except Exception as e:
            # Handle the exception (log the error, raise a custom exception, etc.)
            print(f"MySQL Error: {e}")

        # If an exception occurred or user_profile_data is None, return None
        return None

    
    @classmethod
    def update_user_profile(cls, user_id, name, image_url, bio, facebook, instagram, twitter):
        update_sql = """
            UPDATE userprofile
            SET name = %s, image_url = %s, bio = %s, facebook = %s, instagram = %s, twitter = %s
            WHERE user_id = %s
        """.format(cls.__tablename__)

        try:
            # Use get_db() to get a cursor and connection
            with current_app.app_context():
                connection = mysql.connect()
                cursor = connection.cursor()
                cursor.execute(update_sql, (name, image_url, bio, facebook, instagram, twitter, user_id))
                connection.commit()
        except Exception as e:
            # Handle the exception (log the error, raise a custom exception, etc.)
            print(f"MySQL Error: {e}")
            # Optionally raise a custom exception if you want to propagate it
            # raise CustomException(f"MySQL Error: {e}")

        