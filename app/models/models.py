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

