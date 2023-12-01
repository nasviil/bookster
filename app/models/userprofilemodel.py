from flask import Flask, current_app
from flaskext.mysql import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'sql12663651'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

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
                    return user_profile_data
                else:
                    return None
        except Exception as e:
            # Handle the exception (log the error, raise a custom exception, etc.)
            print(f"MySQL Error: {e}")
            # Optionally raise a custom exception if you want to propagate it
            # raise CustomException(f"MySQL Error: {e}")

        # If an exception occurred, return None or raise an exception as appropriate
        return None