from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('homepage.html')
  
@home.route('/userprofile')
def user_profile():
    return render_template('userprofile.html')
