# app/models/user.py

from app import mysql

class Book:
    __tablename__ = 'Book'

    def __init__(self, book_id=None):
        self.book_id = book_id

    @classmethod
    def get_all_books(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        books = cur.fetchall()
        return books
