import mysql.connector
from flask_login import UserMixin

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'book_app'
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
    def userEmail(self, username):
        cursor = db.cursor()
        sql = "SELECT email FROM users WHERE username  = %s"
        cursor.execute(sql, (username,))
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

