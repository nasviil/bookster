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
    
    user = User.userData(username)
    if user:
      user_name = user[0][1]
      # if check_password_hash(user['password'], password):
      if password == user[0][3]:
          print(user)
          user = User(username)
          session['loggedin']= True
          session['username']= user_name
          login_user(user)
          flash('Login successful!', 'success')
          return jsonify({'success': True})
      else:
        flash('Incorrect password', 'error')
        return jsonify({'success': False, 'message': 'Incorrect password'})
    else:
        flash('User does not exist', 'error')
        return jsonify({'success': False, 'message': 'User does not exist'})


  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))