from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..models.user_book import UserBook
from werkzeug.exceptions import abort


home = Blueprint('home', __name__)

@home.route('/')
def landing_page():
    return render_template("home.html")

@home.route('/home')
@login_required
def home_page():
    return render_template("homepage.html")

@home.route('/<int:user_id>/books')
@login_required
def user_books(user_id):
    user_books = UserBook.get_books_for_user(user_id)
    return render_template('user_books.html', user_books=user_books, user_id=user_id)

@home.route('/<string:username>/books')
@login_required
def username_user_books(username):
    user_books = UserBook.get_books_for_user(username)
    return render_template('user_books.html', user_books=user_books, user_id=username)


@home.route('/<int:user_id>/books/<int:book_id>')
@login_required
def book_detail(user_id, book_id):
    book_detail = UserBook.get_book_details(book_id)
    return render_template('product_detail.html', book_detail=book_detail, user_id=user_id)

@home.route('/<int:user_id>/books/add_book', methods=['GET', 'POST'])
@login_required
def add_book(user_id):
    
    print(f"current_user.id: {current_user.id}")
    print(f"user_id from URL: {user_id}")

    if current_user.id != user_id:
        abort(403)  # Forbidden

    if request.method == 'POST':
        book_title = request.form['book_title']
        book_isbn = request.form['book_isbn']
        book_author = request.form['book_author']
        book_genre = request.form['book_genre']

        UserBook.add_book(user_id, book_title, book_isbn, book_author, book_genre)

        return redirect(url_for('home.user_books', user_id=user_id))

    return render_template('add_book.html', user_id=user_id)
