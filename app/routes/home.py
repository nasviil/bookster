from flask import Blueprint
from flask_login import login_required


home = Blueprint('home', __name__)

@home.route('/')
@login_required
def home_page():
  return "<p>Hello, World!</p>"