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
        SELECT_SQL = f"SELECT u.username, up.* FROM users u INNER JOIN {cls.__tablename__} up ON u.user_id = up.user_id WHERE u.user_id = %s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (user_id,))
        user_profile_data = cur.fetchone()
        return user_profile_data
