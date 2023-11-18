from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User
import re


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  try:
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      
      user = User.userData(username)
      if user:
        user_name = user[0][1]
        if password == user[0][3] or check_password_hash(user[0][3], password):
            print(user)
            user = User(username)
            session['loggedin']= True
            session['username']= user_name
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return jsonify({'success': True})
        else:
          flash('Incorrect password', 'error')
          return jsonify({'success': False, 'message': 'Incorrect password'})
      else:
          flash('User does not exist', 'error')
          return jsonify({'success': False, 'message': 'User does not exist'})
  except Exception as e:
    print(f"Error during login: {str(e)}")
    flash('An error occurred during login. Please try again.', category='error')
    return jsonify({'success': False, 'message': 'An error occurred during login. Please try again.'})
  
  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  try:
    if request.method == 'POST':
      username = request.form.get('username')
      email = request.form.get('email')
      password1 = request.form.get('password1')
      password2 = request.form.get('password2')
      password= generate_password_hash(password1)

      user = User.userData(username)
      existingEmail = User.userEmail(email)
      if user:
        flash('User already exists.', category='error')
        return jsonify({'success': False, 'message': 'User already exists.'})
      elif existingEmail:
        flash('Email already exists.', category='error')
        return jsonify({'success': False, 'message': 'Email already exists.'})
      elif len(username) < 4:
        flash('Username must be at least 4 characters.', category='error')
        return jsonify({'success': False, 'message': 'Username must be at least 4 characters.'})
      elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
          flash('Invalid email address.', category='error')
          return jsonify({'success': False, 'message': 'Invalid email address.'})
      elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
        return jsonify({'success': False, 'message': 'Passwords don\'t match.'})
      elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
        return jsonify({'success': False, 'message': 'Password must be at least 7 characters.'})
      else:
          User.addUser(username, email, password)
          user = User(username)
          session['loggedin']= True
          session['username']= username
          login_user(user, remember=True)
          flash('Account created!', category='success')        
          return jsonify({'success': True})
  except Exception as e:
    print(f"Error during signup: {str(e)}")

    flash('An error occurred during signup. Please try again.', category='error')
    return jsonify({'success': False, 'message': 'An error occurred during signup. Please try again.'})
  return render_template("signup.html", user=current_user)