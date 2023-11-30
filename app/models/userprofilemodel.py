import mysql.connector
from app import mysql

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
        select_sql = """
            SELECT u.username, up.* 
            FROM users u 
            INNER JOIN {} up ON u.user_id = up.user_id 
            WHERE u.user_id = %s
        """.format(cls.__tablename__)

        connection = None  # Initialize the variable

        try:
            connection = mysql.connect()
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(select_sql, (user_id,))
                user_profile_data = cursor.fetchone()
                return user_profile_data
        except Exception as e:
            # Handle the exception (print/log the error, raise it, etc.)
            print(f"Error: {e}")
            # Optionally re-raise the exception if you want to propagate it
            # raise
        finally:
            if connection:
                connection.close()
