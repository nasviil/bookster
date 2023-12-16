import mysql.connector
from flask_login import UserMixin
from app.models.userprofilemodel import UserProfile 

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'sql12663651'
)
cursor = db.cursor()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)

    @classmethod
    def userList(cls):
        cursor = db.cursor()
        sql = "SELECT * from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @classmethod
    def addUser(self, username, email, password):
        cursor = db.cursor()
        sql = f"INSERT INTO users(username, email, password) \
               VALUES('{username}', '{email}', '{password}')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        
    @classmethod
    def addUserProfile(cls, user_id, name="", image_url="", bio="", facebook="", instagram="", twitter=""):
        cursor = db.cursor()
        sql = "INSERT INTO userprofile (user_id, name, image_url, bio, facebook, instagram, twitter) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, name, image_url, bio, facebook, instagram, twitter))
        db.commit()
        cursor.close()

                
    @classmethod
    def deleteUser(cls, username):
        cursor = db.cursor()
        sql = f"DELETE FROM users WHERE username='{username}'"
        cursor.execute(sql)
        db.commit()
        cursor.close()

    @classmethod
    def userData(self, username):
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE username  = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @classmethod
    def userData1(self, user_id):
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE user_id  = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    

    @classmethod
    def get(cls, user_id):
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE user_id = %s"  # Replace 'user_id' with your actual column name
        cursor.execute(sql, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            # If 'user_id' is the first element in the tuple, you can access it using index 0
            return User(id=user_data[0])  # Replace 0 with the correct index
        return None

    @classmethod
    def userEmail(self, email):
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE email  = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @classmethod
    def userID(self, id):
        cursor = db.cursor()
        sql = "SELECT id FROM users WHERE id  = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @classmethod
    def userID1(self, username):
        cursor = db.cursor()
        sql = "SELECT user_id FROM users WHERE username  = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    

    @classmethod
    def verify_email(cls, user_id):
        cursor = db.cursor()
        sql = "UPDATE users SET email_verified = TRUE WHERE id = %s"
        cursor.execute(sql, (user_id,))
        db.commit()
        cursor.close()

class User_Verification_Data(UserMixin):
    def __init__(self, id):
        self.id = id

    @classmethod
    def addVerify_Data(self, username, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num):
        cursor = db.cursor()
        sql = """
            INSERT INTO users_verification_data
                (username, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (username, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

    @classmethod
    def updateVerify_Data(cls, username, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num):
        cursor = db.cursor()
        sql = """
            UPDATE users_verification_data
            SET firstname = %s, lastname = %s, gender = %s, birthday = %s, address = %s,
                mailAddress = %s, contactnum = %s, id_upload = %s, id_type = %s, id_num = %s
            WHERE username = %s
        """
        values = (firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num, username)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

    @classmethod
    def updateVerifyCode(cls, user_id):
        cursor = db.cursor()
        sql = f"UPDATE users SET verify_code = TRUE WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        


