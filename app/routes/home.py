from flask import Blueprint, render_template
from flask_login import login_required
from ..models.user_book import UserBook


home = Blueprint('home', __name__)

@home.route('/')
@login_required
def home_page():
    return render_template("homepage.html")

@home.route('/<int:user_id>/books')
@login_required
def user_books(user_id):
    user_books = UserBook.get_books_for_user(user_id)
    return render_template('user_books.html', user_books=user_books, user_id=user_id)


@home.route('/<int:user_id>/books/<int:book_id>')
@login_required
def book_detail(user_id, book_id):
    book_detail = UserBook.get_book_details(book_id)
    return render_template('product_detail.html', book_detail=book_detail, user_id=user_id)
