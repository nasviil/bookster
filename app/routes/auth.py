from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    
    user = User.userEmail(username)
    if user:
      user_id = user[0][0]
      # if check_password_hash(user['password'], password):
      if password == user[0][3]:
          print(user)
          # is_active = True
          # user = User(user_id, is_active)  # Create a User object or equivalent
          login_user(user_id, remember=True)
          flash('Login successful!', 'success')
          return redirect(url_for('home.home_page')) 
      else:
        flash('Incorrect password', 'error')
    else:
        flash('User does not exist', 'error')

  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))