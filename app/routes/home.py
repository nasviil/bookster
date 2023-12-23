from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,abort
from flask_login import login_required, current_user
from ..models.user_book import UserBook, Genre, Address, Region
from ..models.userprofilemodel import UserProfile
from werkzeug.exceptions import abort
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
from flask_paginate import Pagination
from ..models.models import User

home = Blueprint('home', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg'}
MAX_FILE_SIZE = 1 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@home.route('/')
def landing_page():
    return render_template("home.html")

@home.route('/home')
@login_required
def home_page():
    return render_template("homepage.html")

@home.route('/books', methods=['GET'])
@login_required
def all_books():
    current_user.id = int(current_user.id)
    books = UserBook.get_all_books()
    genres = Genre.get_genres()
    selected_genre = request.args.get('genre', 'all')
    search_query = request.args.get('search', '')

    if selected_genre != 'all':
        books = [book for book in books if book['book_genre'] == int(selected_genre)]

    if search_query:
        # If there's a search query, filter the books based on it
        books = [book for book in books if search_query.lower() in book['book_title'].lower()]

    unique_books = {}  # Use a dictionary to store unique books based on book_id

    for book in books:
        if current_user.id != book['user_id']:
            if book['book_id'] not in unique_books:
                unique_books[book['book_id']] = book

    # Extract values (unique books) from the dictionary
    other_books = list(unique_books.values())

    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(other_books) + per_page - 1) // per_page

    items_on_page = other_books[start:end]

    return render_template('library.html', genres=genres, other_books=other_books, items_on_page=items_on_page, total_pages=total_pages, page=page, search_query=search_query, selected_genre=selected_genre)

@home.route('/<int:user_id>/orders', methods=['GET', 'POST'])
@login_required
def order_page(user_id):
    current_user.id = int(current_user.id)
    buy_orders = None
    book_detail = None
    buyer = None

    if current_user.id == user_id:
        buy_orders = UserBook.get_purchase_orders(user_id)
        if buy_orders is not None:
            book_detail = [UserBook.get_book_details(order['book_id']) for order in buy_orders]
            buyer = [User.userData1(order['buyer_id']) for order in buy_orders]

        if request.method == 'POST':
            confirm_button_clicked = 'confirm_button' in request.form
            reject_button_clicked = 'reject_button' in request.form

            if confirm_button_clicked:
                buyer_id = request.form.get('buyer_id')
                seller_id = request.form.get('seller_id')
                book_id = request.form.get('book_id')
                UserBook.confirm_purchase_order(buyer_id, seller_id, book_id)
                flash('Purchase confirmed successfully!', 'success')

            return redirect(url_for('home.order_page', user_id=user_id))

    return render_template('order_page.html', user_id=user_id, buy_orders=buy_orders, book_detail=book_detail, buyer=buyer)



@home.route('/<int:user_id>/books')
@login_required
def user_books(user_id):
    user_books = UserBook.get_books_for_user(user_id)
    user_profile_data = UserProfile.get_user_profile(user_id)
    user = User.userData1(user_id)
    genres = Genre.get_genres()
    selected_genre = request.args.get('genre', 'all')
    if selected_genre != 'all':
        user_books = [book for book in user_books if book['book_genre'] == int(selected_genre)]

    page = request.args.get('page', 1, type=int)
    per_page = 40
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(user_books) + per_page - 1) // per_page

    items_on_page = user_books[start:end]

    return render_template('user_books.html', user_profile_data= user_profile_data, user_books=user_books, user_id=user_id, genres=genres,  items_on_page=items_on_page, total_pages=total_pages, page=page, user=user)

@home.route('/books/<int:book_id>')
@login_required
def book_detail(book_id):
    books = UserBook.get_all_books()
    matching_book = None
    book_detail = None
    
    # Assuming current_user.id is an integer
    current_user_id = int(current_user.id)
    
    for book in books:
        if book['book_id'] == book_id and book['user_id'] != current_user_id:
            # Assuming book_detail should be details for the other user and the specific book
            book_detail = UserBook.get_book_user_details(book['user_id'], book_id)
            matching_book = book
            break
    
    print(matching_book)
    
    return render_template('library-detail.html', book_detail=book_detail, books=books, matching_book=matching_book)


@home.route('/<int:user_id>/books/<int:book_id>')
@login_required
def book_user_detail(user_id, book_id):
    current_user.id = int(current_user.id)
    books = UserBook.get_all_books()
    book_detail = UserBook.get_book_user_details(user_id, book_id)

    # Filter out the current book from the list
    other_books = [book for book in books if book['book_id'] == book_id and book['user_id'] != user_id and book['user_id'] != current_user.id]

    return render_template('product_detail.html', book_detail=book_detail, user_id=user_id, other_books=other_books)


@home.route('/<int:user_id>/books/<int:book_id>/buy',  methods=['GET', 'POST'])
@login_required
def book_buy(user_id, book_id):
    books = UserBook.get_all_books()
    matching_book = None
    book_detail = None
    current_user_id = int(current_user.id)
    
    for book in books:
        if book['book_id'] == book_id and book['user_id'] != current_user_id:
            book_detail = UserBook.get_book_user_details(book['user_id'], book_id)
            matching_book = book
            break

    if request.method == 'POST':
        buyer_id = current_user_id
        book_id = matching_book['book_id']
        seller_id = matching_book['user_id']
        quantity = request.form['quantity']

        UserBook.add_purchase_order(buyer_id, book_id, seller_id, quantity)

        return redirect(url_for('home.user_books', user_id=user_id))
    
    return render_template('buycheckout.html', book_detail=book_detail, books=books, matching_book=matching_book, user_id=user_id)

@home.route('/<int:user_id>/books/add_book', methods=['GET', 'POST'])
@login_required
def add_book(user_id):
    current_user.id = int(current_user.id)
    if current_user.id != user_id:
        abort(403)  # Forbidden

    if request.method == 'POST':
        book_title = request.form['book_title']
        book_isbn = request.form['book_isbn']
        book_author = request.form['book_author']
        book_genre = request.form['book_genre']
        selling_price = request.form['selling_price']
        renting_price = request.form['renting_price']
        quantity = request.form['quantity']

        if 'book_image' in request.files:
            uploaded_file = request.files['book_image']
            if uploaded_file and allowed_file(uploaded_file.filename):
                cloudinary_response = cloudinary.uploader.upload(uploaded_file)
                cloudinary_url = cloudinary_response.get('secure_url', '')

                UserBook.add_book(user_id, book_title, book_isbn, book_author, book_genre, cloudinary_url, selling_price, renting_price, quantity)

        return redirect(url_for('home.user_books', user_id=user_id))

    genres = Genre.get_genres()

    return render_template('add_book.html', user_id=user_id, genres=genres)

@home.route('/<int:user_id>/books/delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(user_id, book_id):
    UserBook.delete_book(user_id, book_id)
    return redirect(url_for('home.user_books', user_id=user_id))

@home.route('/<int:user_id>/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(user_id, book_id):
    current_user.id = int(current_user.id)
    if current_user.id != user_id:
        abort(403)  # Forbidden

    book_detail = UserBook.get_book_user_details(user_id, book_id)

    if request.method == 'POST':
        print("Form data received:", request.form)
        book_title = request.form['book_title']
        book_isbn = request.form['book_isbn']
        book_author = request.form['book_author']
        book_genre = request.form['book_genre']
        selling_price = request.form['selling_price']
        renting_price = request.form['renting_price']
        quantity = request.form['quantity']
        cloudinary_url = ''  # Initialize with an empty string by default

        if 'book_image' in request.files:
            uploaded_file = request.files['book_image']
            if uploaded_file and allowed_file(uploaded_file.filename):
                cloudinary_response = cloudinary.uploader.upload(uploaded_file)
                cloudinary_url = cloudinary_response.get('secure_url', '')
            else:
                # Update cloudinary_url only if book_detail is available
                if book_detail and 'cloudinary_url' in book_detail:
                    cloudinary_url = book_detail['cloudinary_url']

        UserBook.edit_book(
            book_id,
            book_title,
            book_isbn,
            book_author,
            book_genre,
            selling_price,
            renting_price,
            cloudinary_url,
            user_id,
            quantity
        )
        return redirect(url_for('home.book_user_detail', book_detail=book_detail, user_id=user_id, book_id=book_id))

    genres = Genre.get_genres()
    return render_template('edit-book.html', book_detail=book_detail, user_id=user_id, genres=genres)


@home.route('/<int:user_id>/books/<int:book_id>/buy/checkout/add_address', methods=['GET', 'POST'])
@login_required
def add_address(user_id, book_id):
    current_user_id = current_user.id

    if request.method == 'POST':
        # Retrieve form data
        fullname = request.form['fullname']
        phone_number = request.form.get('phone_number', '')
        region_id = request.form['region']
        province = request.form['province']
        city = request.form['city']
        barangay = request.form['barangay']
        zipcode = request.form.get('zipcode', '')
        house_no = request.form.get('house_no', '')
        notes = request.form.get('notes', '')  # Optional field, use get() to avoid KeyError

        # Add the new address to the database
        address_id = Address.add_address(user_id, fullname, phone_number, region_id, province, city, barangay, zipcode, house_no, notes)

        # Assuming Address.add_address() returns the address_id
        if address_id:
            # Address added successfully, redirect to the checkout page
            return redirect(url_for('home.buy_checkout', user_id=user_id, book_id=book_id))
        else:
            # Handle the case where the address was not added
            return jsonify({'error': 'Failed to add address'}), 500  # Internal Server Error
    elif request.method == 'GET':
        # Fetch regions from the database
        regions = Region.get_region()

        # Render the address.html template for adding a new address with regions data
        return render_template('address.html', user_id=user_id, book_id=book_id, regions=regions)
    else:
        # Handle other request methods if needed
        return jsonify({'message': 'Method not allowed'}), 405  # Method Not Allowed

@home.route('/<int:user_id>/books/<int:book_id>/buy/checkout', methods=['GET', 'POST'])
@login_required
def buy_checkout(user_id, book_id):
   books = UserBook.get_all_books()
   matching_book = None
   book_detail = None
   
   # Assuming current_user.id is an integer
   current_user_id = int(current_user.id)
   
   for book in books:
       if book['book_id'] == book_id and book['user_id'] != current_user_id:
           # Assuming book_detail should be details for the other user and the specific book
           book_detail = UserBook.get_book_user_details(book['user_id'], book_id)
           matching_book = book
           break
       
   return render_template('buycheckout.html', book_detail=book_detail, books=books, matching_book=matching_book, user_id=user_id)
