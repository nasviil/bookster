# from flask import Flask
# from flaskext.mysql import MySQL
from datetime import datetime
from app import mysql

# app = Flask(__name__)
# # Configure MySQL
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_DB'] = 'sql12663651'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost' 


# mysql = MySQL(app)


class UserBook:
    __tablename__ = 'user_book_instances'

    def __init__(self, user_book_id=None, user_id=None, book_id=None):
        self.user_book_id = user_book_id
        self.user_id = user_id
        self.book_id = book_id

    @classmethod
    def get_books_for_user(cls, user_id):
        SELECT_SQL = f"SELECT books.* FROM {cls.__tablename__} JOIN books ON {cls.__tablename__}.book_id = books.book_id WHERE {cls.__tablename__}.user_id = %s ORDER BY books.book_title ASC"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (user_id,))
        books = cur.fetchall()
        return books
    
    @classmethod
    def get_book_details(cls, book_id):
        SELECT_SQL = f"SELECT *, users.* FROM {cls.__tablename__} \
                    JOIN books ON {cls.__tablename__}.book_id = books.book_id \
                    JOIN genre ON books.book_genre = genre.genre_id \
                    JOIN users ON {cls.__tablename__}.user_id = users.user_id \
                    WHERE {cls.__tablename__}.book_id = %s"

        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (book_id,))
        book_detail = cur.fetchone()
        return book_detail
    
    @classmethod
    def add_book(cls, user_id, book_title, book_isbn, book_author, book_genre, book_sell_price, book_rent_price, cloudinary_url):
            INSERT_BOOK_SQL = (
                "INSERT INTO books (book_title, book_isbn, book_author, book_genre, date_added, book_sell_price, book_rent_price, cloudinary_url) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            INSERT_INSTANCE_SQL = "INSERT INTO user_book_instances (user_id, book_id) VALUES (%s, %s)"

            cur = mysql.connection.cursor()

            try:
                # Start a transaction
                cur.execute("START TRANSACTION")

                # Insert into books
                cur.execute(INSERT_BOOK_SQL, (book_title, book_isbn, book_author, book_genre, datetime.now(), book_sell_price, book_rent_price, cloudinary_url))
                book_id = cur.lastrowid

                # Insert into user_book_instances
                cur.execute(INSERT_INSTANCE_SQL, (user_id, book_id))

                # Commit the transaction
                mysql.connection.commit()
            except Exception as e:
                # Rollback the transaction in case of an error
                mysql.connection.rollback()
                raise e
            finally:
                # Close the cursor
                cur.close()

    @classmethod
    def delete_book(cls, user_id, book_id):
        DELETE_BOOK_SQL = "DELETE FROM books WHERE book_id = %s"
        DELETE_INSTANCE_SQL = "DELETE FROM user_book_instances WHERE user_id = %s AND book_id = %s"

        cur = mysql.connection.cursor()

        try:
            # Start a transaction
            cur.execute("START TRANSACTION")

            # Delete from user_book_instances
            cur.execute(DELETE_INSTANCE_SQL, (user_id, book_id))

            # Delete from books
            cur.execute(DELETE_BOOK_SQL, (book_id,))

            # Commit the transaction
            mysql.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            mysql.connection.rollback()
            raise e
        finally:
            # Close the cursor
            cur.close()

    @classmethod
    def edit_book(cls, book_id, book_title, book_isbn, book_author, book_genre, book_sell_price, book_rent_price, cloudinary_url):
        UPDATE_BOOK_SQL = (
            "UPDATE books SET "
            "book_title=%s, book_isbn=%s, book_author=%s, book_genre=%s, "
            "book_sell_price=%s, book_rent_price=%s, cloudinary_url=%s "
            "WHERE book_id=%s"
        )

        cur = mysql.connection.cursor()

        try:
            # Update the books table
            cur.execute(UPDATE_BOOK_SQL, (book_title, book_isbn, book_author, book_genre, book_sell_price, book_rent_price, cloudinary_url, book_id))

            # Commit the transaction
            mysql.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            mysql.connection.rollback()
            raise e
        finally:
            # Close the cursor
            cur.close()


class Genre:
    __tablename__ = 'genre'

    @classmethod
    def get_genres(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        genres = cur.fetchall()
        return genres