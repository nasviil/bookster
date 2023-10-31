from flask import Blueprint


home = Blueprint('home', __name__)

@home.route('/')
def home_page():
  return "<p>Hello, World!</p>"