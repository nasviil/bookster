from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template("product_detail.html")