#from flask import Flask
#from flaskext.mysql import MySQL
from datetime import datetime
from app import mysql

#app = Flask(__name__)
# # Configure MySQL
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
#app.config['MYSQL_DATABASE_DB'] = 'sql12663651'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost' 


#Mysql = MySQL(app)

class UserBook:
    __tablename__ = 'user_book_instances'

    def __init__(self, user_book_id=None, user_id=None, book_id=None):
        self.user_book_id = user_book_id
        self.user_id = user_id
        self.book_id = book_id


    @classmethod
    def get_all_books(cls):
        SELECT_ALL_SQL = """
            SELECT books.*, user_book_instances.user_id
            FROM books
            LEFT JOIN user_book_instances ON books.book_id = user_book_instances.book_id
            ORDER BY books.book_title ASC
        """
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_ALL_SQL)
        books = cur.fetchall()
        return books

    @classmethod
    def get_books_for_user(cls, user_id):
        SELECT_SQL = f"SELECT books.* FROM {cls.__tablename__} JOIN books ON {cls.__tablename__}.book_id = books.book_id WHERE {cls.__tablename__}.user_id = %s ORDER BY books.book_title ASC"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (user_id,))
        books = cur.fetchall()
        return books

    
    @classmethod
    def get_book_user_details(cls, user_id, book_id):
        SELECT_SQL = f"SELECT DISTINCT {cls.__tablename__}.*, books.*, genre.*, users.* \
                    FROM {cls.__tablename__} \
                    JOIN books ON {cls.__tablename__}.book_id = books.book_id \
                    JOIN genre ON books.book_genre = genre.genre_id \
                    JOIN users ON {cls.__tablename__}.user_id = users.user_id \
                    WHERE {cls.__tablename__}.book_id = %s AND {cls.__tablename__}.user_id = %s"

        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (book_id, user_id))
        book_detail = cur.fetchone()
        return book_detail
    
    @classmethod
    def get_book_details(cls, book_id):
        try:
            SELECT_BOOK_SQL = "SELECT * FROM books WHERE book_id = %s"
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_BOOK_SQL, (int(book_id),))
            book_details = cur.fetchone()
            return book_details
        except Exception as e:
            print(f"Error in get_book_details: {e}")
            return None

    @classmethod
    def get_purchase_orders(cls, seller_id):
        try:
            SELECT_ORDERS_SQL = (
                "SELECT * FROM purchase_books "
                "WHERE seller_id = %s AND is_confirmed = 0"
            )
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_ORDERS_SQL, (seller_id,))
            book_orders = cur.fetchall()
            return book_orders
        except Exception as e:
            print(f"Error in get_purchase_orders: {e}")
            return None

    @classmethod
    def get_user_purchase(cls, buyer_id):
        try:
            SELECT_ORDERS_SQL = (
                "SELECT * FROM purchase_books "
                "WHERE buyer_id = %s AND is_confirmed = 1"
            )
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_ORDERS_SQL, (buyer_id,))
            confirmed_orders = cur.fetchall()
            return confirmed_orders
        except Exception as e:
            print(f"Error in get_purchase_orders: {e}")
            raise

    @classmethod
    def get_confirmed_purchase_orders(cls, seller_id):
        try:
            SELECT_ORDERS_SQL = (
                "SELECT * FROM purchase_books "
                "WHERE seller_id = %s AND is_confirmed = 1"
            )
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_ORDERS_SQL, (seller_id,))
            confirmed_orders = cur.fetchall()
            return confirmed_orders
        except Exception as e:
            print(f"Error in get_purchase_orders: {e}")
            return None
        
    @classmethod
    def get_confirmed_rent_orders(cls, owner_id):
        try:
            SELECT_ORDERS_SQL = (
                "SELECT * FROM rent_books "
                "WHERE owner_id = %s AND is_rented = 1"
            )
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_ORDERS_SQL, (owner_id,))
            confirmed_orders = cur.fetchall()
            return confirmed_orders
        except Exception as e:
            print(f"Error in get_purchase_orders: {e}")
            return None
        
    @classmethod
    def confirm_return_rent(cls, owner_id, book_id, rent_id):
        try:
            # Start a transaction
            with mysql.connection.cursor() as cur:
                # Update rent_books table
                CONFIRM_RETURN_SQL = "UPDATE rent_books SET is_returned = 1 WHERE rent_id = %s"
                cur.execute(CONFIRM_RETURN_SQL, (rent_id,))

                # Increment quantity in user_book_instances table
                UPDATE_QUANTITY_SQL = (
                    "UPDATE user_book_instances SET quantity = quantity + 1 "
                    "WHERE user_id = %s AND book_id = %s"
                )
                cur.execute(UPDATE_QUANTITY_SQL, (owner_id, book_id))

            # Commit the transaction
            mysql.connection.commit()
        except Exception as e:
            # Handle exceptions (rollback, log, etc.)
            mysql.connection.rollback()
            print(f"Error confirming return: {e}")
        finally:
            # Close the cursor (optional)
            cur.close()

    @classmethod
    def get_user_rents(cls, renter_id):
        try:
            SELECT_ORDERS_SQL = (
                "SELECT * FROM rent_books "
                "WHERE renter_id = %s AND is_rented = 1"
            )
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_ORDERS_SQL, (renter_id,))
            confirmed_orders = cur.fetchall()
            return confirmed_orders
        except Exception as e:
            print(f"Error in get_purchase_orders: {e}")
            return None

    @classmethod
    def add_purchase_order(cls, buyer_id, book_id, seller_id, quantity):
        INSERT_ORDER_SQL = ("INSERT INTO purchase_books (buyer_id, book_id, seller_id, quantity, purchase_date)""VALUES(%s, %s, %s, %s, %s)");
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(INSERT_ORDER_SQL, (buyer_id, book_id, seller_id, quantity, datetime.now()))
        mysql.connection.commit()

    @classmethod
    def delete_purchase_order(cls, purchase_id):
        DELETE_ORDER_SQL = "DELETE FROM purchase_books WHERE purchase_id = %s"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(DELETE_ORDER_SQL, (purchase_id,))  # Add the tuple parentheses
        mysql.connection.commit()

    @classmethod
    def delete_rent_order(cls, rent_id):
        DELETE_ORDER_SQL = "DELETE FROM rent_books WHERE rent_id = %s"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(DELETE_ORDER_SQL, (rent_id,))  # Add the tuple parentheses
        mysql.connection.commit()

    @classmethod
    def confirm_purchase_order(cls, buyer_id, seller_id, book_id):
        cur = mysql.connection.cursor(dictionary=True)
        try:
            # Retrieve the quantity from purchase_books
            SELECT_PURCHASE_BOOK_SQL = (
                "SELECT quantity FROM purchase_books "
                "WHERE buyer_id = %s AND seller_id = %s AND book_id = %s AND is_confirmed = 0"
            )
            cur.execute(SELECT_PURCHASE_BOOK_SQL, (buyer_id, seller_id, book_id))
            purchase_info = cur.fetchone()

            if purchase_info:
                purchase_quantity = purchase_info['quantity']

                # Update purchase_books
                UPDATE_PURCHASE_BOOK_SQL = (
                    "UPDATE purchase_books "
                    "SET is_confirmed = 1 "
                    "WHERE buyer_id = %s AND seller_id = %s AND book_id = %s"
                )
                cur.execute(UPDATE_PURCHASE_BOOK_SQL, (buyer_id, seller_id, book_id))
                mysql.connection.commit()

                # Retrieve the user_book_id and quantity from user_book_instances
                SELECT_USER_BOOK_SQL = (
                    "SELECT user_book_id, quantity FROM user_book_instances "
                    "WHERE user_id = %s AND book_id = %s"
                )
                cur.execute(SELECT_USER_BOOK_SQL, (seller_id, book_id))
                user_book_info = cur.fetchone()

                if user_book_info:
                    user_book_id = user_book_info['user_book_id']
                    original_quantity = user_book_info['quantity']

                    # Subtract purchase quantity from user_book_instances quantity
                    new_quantity = max(original_quantity - purchase_quantity, 0)

                    # Update user_book_instances
                    UPDATE_USER_BOOK_SQL = (
                        "UPDATE user_book_instances SET quantity = %s WHERE user_book_id = %s"
                    )
                    cur.execute(UPDATE_USER_BOOK_SQL, (new_quantity, user_book_id))
                    mysql.connection.commit()

        except Exception as e:
            print(f"Error updating purchase order: {e}")
        finally:
            cur.close()
            
            
    @classmethod
    def get_rent_orders(cls, seller_id):
        try:
            SELECT_ORDERS_SQL = (
                "SELECT * FROM rent_books "
                "WHERE owner_id = %s AND is_rented = 0 AND is_returned = 0"
            )
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute(SELECT_ORDERS_SQL, (seller_id,))
            book_orders = cur.fetchall()
            return book_orders
        except Exception as e:
            print(f"Error in get_rent_orders: {e}")
            return None

    @classmethod
    def add_rent_order(cls, renter_id, book_id, owner_id, quantity, rent_start_date, rent_end_date):
        INSERT_ORDER_SQL = ("INSERT INTO rent_books (renter_id, book_id, owner_id, quantity, rent_start_date, rent_end_date)""VALUES(%s, %s, %s, %s, %s, %s)");
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(INSERT_ORDER_SQL, (renter_id, book_id, owner_id, quantity,  rent_start_date, rent_end_date))
        mysql.connection.commit()

    @classmethod
    def confirm_rent_order(cls, renter_id, owner_id, book_id):
        UPDATE_ORDER_SQL = (
            "UPDATE rent_books SET is_rented = 1 WHERE renter_id = %s AND owner_id = %s AND book_id = %s"
        )
        cur = mysql.connection.cursor(dictionary=True)
        try:
            # Print debug info
            print("Debug Info:", renter_id, owner_id, book_id)

            # Update purchase_books
            cur.execute(UPDATE_ORDER_SQL, (renter_id, owner_id, book_id))
            mysql.connection.commit()

            # Subtract quantity from user_book_instances
            SELECT_USER_BOOK_SQL = (
                "SELECT user_book_id, quantity FROM user_book_instances "
                "WHERE user_id = %s AND book_id = %s"
            )
            cur.execute(SELECT_USER_BOOK_SQL, (owner_id, book_id))
            user_book_info = cur.fetchone()

            if user_book_info:
                user_book_id = user_book_info['user_book_id']
                original_quantity = user_book_info['quantity']
                # Subtract quantity
                new_quantity = max(original_quantity - 1, 0)  # Ensure it doesn't go below 0

                UPDATE_USER_BOOK_SQL = (
                    "UPDATE user_book_instances SET quantity = %s WHERE user_book_id = %s"
                )
                cur.execute(UPDATE_USER_BOOK_SQL, (new_quantity, user_book_id))
                mysql.connection.commit()

        except Exception as e:
            print(f"Error updating purchase order: {e}")
        finally:
            cur.close()



    @classmethod
    def add_book(cls, user_id, book_title, book_isbn, book_author, book_genre, cloudinary_url, selling_price, renting_price, quantity):
        INSERT_BOOK_SQL = (
            "INSERT INTO books (book_title, book_isbn, book_author, book_genre, book_added, cloudinary_url) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        INSERT_INSTANCE_SQL = (
            "INSERT INTO user_book_instances (user_id, book_id, selling_price, renting_price, quantity) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        SELECT_BOOK_SQL = "SELECT book_id FROM books WHERE book_isbn = %s"

        cur = mysql.connection.cursor()

        try:
            # Start a transaction
            cur.execute("START TRANSACTION")

            # Check if the book with the given ISBN already exists
            cur.execute(SELECT_BOOK_SQL, (book_isbn,))
            existing_book = cur.fetchone()

            if existing_book:
                # If the book exists, use its book_id
                book_id = existing_book[0]
            else:
                # Insert into books
                cur.execute(INSERT_BOOK_SQL, (book_title, book_isbn, book_author, book_genre, datetime.now(), cloudinary_url))
                book_id = cur.lastrowid

            # Insert into user_book_instances
            cur.execute(INSERT_INSTANCE_SQL, (user_id, book_id, selling_price, renting_price, quantity))

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
    def edit_book(cls, book_id, book_title, book_isbn, book_author, book_genre, selling_price, renting_price, cloudinary_url, user_id, quantity):
        UPDATE_BOOK_SQL = (
            "UPDATE books "
            "SET book_title=%s, book_isbn=%s, book_author=%s, book_genre=%s, cloudinary_url=%s "
            "WHERE book_id=%s"
        )
        UPDATE_INSTANCE_SQL = (
            "UPDATE user_book_instances "
            "SET selling_price=%s, renting_price=%s, quantity=%s "
            "WHERE user_id=%s AND book_id=%s"
        )

        cur = mysql.connection.cursor()

        try:
            # Start a transaction
            cur.execute("START TRANSACTION")

            # Update the book record
            cur.execute(
                UPDATE_BOOK_SQL,
                (book_title, book_isbn, book_author, book_genre, cloudinary_url, book_id),
            )

            # Update the user_book_instances record
            cur.execute(
                UPDATE_INSTANCE_SQL,
                (selling_price, renting_price, quantity, user_id, book_id),
            )

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
    
class Region:
    __tablename__ = 'region'

    @classmethod
    def get_region(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        regions = cur.fetchall()
        return regions
    
class Address:
    __tablename__ = 'address'

    @classmethod
    def get_address(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        addresses = cur.fetchall()
        return addresses

    @classmethod
    def get_user_addresses(cls, user_id):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__} WHERE user_id = %s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (user_id,))
        user_addresses = cur.fetchall()
        return user_addresses

    @classmethod
    def add_address(cls, address_id, user_id, fullname, phone_number, region_id, province, city, barangay, zipcode, street, building, house_no, notes):
        INSERT_SQL = (
            "INSERT INTO address "
            "(address_id, user_id, fullname, phone_number, region_id, province, city, barangay, zipcode, street, building, house_no, notes) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        cur = mysql.connection.cursor()
        try:
            cur.execute(INSERT_SQL, (address_id, user_id, fullname, phone_number, region_id, province, city, barangay, zipcode, street, building, house_no, notes))
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cur.close()

    
class BuyReq:
    __tablename__ = 'buyrequest'
    
    def __init__(self, request_id, user_id, quantity, subtotal, total, book_id, region_id, method_id):
        self.request_id = request_id
        self.user_id = user_id
        self.quantity = quantity
        self.subtotal = subtotal
        self.total = total
        self.book_id = book_id
        self.region_id = region_id
        self.method_id = method_id

