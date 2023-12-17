from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.user_book import UserBook, Genre
from ..models.userprofilemodel import UserProfile
from werkzeug.exceptions import abort
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename

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

@home.route('/books')
@login_required
def all_books():
    books = UserBook.get_all_books()
    genres = Genre.get_genres()
    selected_genre = request.args.get('genre', 'all')
    if selected_genre != 'all':
        books = [book for book in books if book['book_genre'] == int(selected_genre)]
    return render_template('library.html', books=books, genres=genres)

@home.route('/<int:user_id>/books')
@login_required
def user_books(user_id):
    user_books = UserBook.get_books_for_user(user_id)
    user_profile_data = UserProfile.get_user_profile(user_id)
    genres = Genre.get_genres()
    selected_genre = request.args.get('genre', 'all')
    if selected_genre != 'all':
        user_books = [book for book in user_books if book['book_genre'] == int(selected_genre)]

    return render_template('user_books.html', user_profile_data= user_profile_data, user_books=user_books, user_id=user_id, genres=genres)

# @home.route('/<string:username>/books')
# @login_required
# def username_user_books(username):
#     user_books = UserBook.get_books_for_user(username)
#     return render_template('user_books.html', user_books=user_books, user_id=username)

@home.route('/books/<int:book_id>')
@login_required
def book_detail(book_id):
    books = UserBook.get_all_books()
    book_detail = UserBook.get_book_details(book_id)
    matching_book = None
    for book in books:
        if book['user_id'] == book_detail['user_id']:
            matching_book = book
            break
    print(matching_book)
    return render_template('library-detail.html', book_detail=book_detail, books=books, matching_book=matching_book)


@home.route('/<int:user_id>/books/<int:book_id>')
@login_required
def book_user_detail(user_id, book_id):
    book_detail = UserBook.get_book_details(book_id)
    return render_template('product_detail.html', book_detail=book_detail, user_id=user_id)

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
        book_sell_price = request.form['book_sell_price']
        book_rent_price = request.form['book_rent_price']

        if 'book_image' in request.files:
            uploaded_file = request.files['book_image']
            if uploaded_file and allowed_file(uploaded_file.filename):
                cloudinary_response = cloudinary.uploader.upload(uploaded_file)
                cloudinary_url = cloudinary_response.get('secure_url', '')

                UserBook.add_book(user_id, book_title, book_isbn, book_author, book_genre, book_sell_price, book_rent_price, cloudinary_url)

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
    if current_user.id != user_id:
        abort(403)  # Forbidden

    book_detail = UserBook.get_book_details(book_id)

    if request.method == 'POST':
        print("Form data received:", request.form)
        book_title = request.form['book_title']
        book_isbn = request.form['book_isbn']
        book_author = request.form['book_author']
        book_genre = request.form['book_genre']
        book_sell_price = request.form['book_sell_price']
        book_rent_price = request.form['book_rent_price']
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
            book_sell_price,
            book_rent_price,
            cloudinary_url
        )
        return redirect(url_for('home.book_detail', book_detail=book_detail, user_id=user_id, book_id=book_id))

    genres = Genre.get_genres()
    return render_template('edit-book.html', book_detail=book_detail, user_id=user_id, genres=genres)
