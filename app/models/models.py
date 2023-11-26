import mysql.connector
from flask_login import UserMixin

db = mysql.connector.connect(
    host = 'sql12.freesqldatabase.com',
    user = 'sql12663651',
    password = 'xJ7bV16PAQ',
    database = 'sql12663651'
)
cursor = db.cursor()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

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
    
class User_Verification_Data(UserMixin):
    def __init__(self, id):
        self.id = id

    @classmethod
    def addVerify_Data(self, user_id, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num):
        cursor = db.cursor()
        sql = """
            INSERT INTO users_verification_data
                (user_id, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (user_id, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

    @classmethod
    def updateVerify_Data(cls, user_id, firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num):
        cursor = db.cursor()
        sql = """
            UPDATE users_verification_data
            SET firstname = %s, lastname = %s, gender = %s, birthday = %s, address = %s,
                mailAddress = %s, contactnum = %s, id_upload = %s, id_type = %s, id_num = %s
            WHERE user_id = %s
        """
        values = (firstname, lastname, gender, birthday, address, mailAddress, contactnum, id_upload, id_type, id_num, user_id)
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


