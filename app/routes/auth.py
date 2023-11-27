from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User, User_Verification_Data
import re
import os
import cloudinary
import cloudinary.api
import cloudinary.uploader
import requests

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
        user_id = user[0][0]
        if password == user[0][3] or check_password_hash(user[0][3], password):
            user = User(user_id)
            session['loggedin']= True
            session['username']= user_name
            session['user_id']= user_id
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
        user_id =user[0][0]
        user_name =user[0][1]        
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
          user = User(user_id)
          session['loggedin']= True
          session['username']= username
          #session['user_id']= User.get_id()
          login_user(user, remember=True)
          flash('Account created!', category='success')        
          return jsonify({'success': True})
  except Exception as e:
    print(f"Error during signup: {str(e)}")

    flash('An error occurred during signup. Please try again.', category='error')
    return jsonify({'success': False, 'message': 'An error occurred during signup. Please try again.'})
  return render_template("signup.html", user=current_user)


@auth.route('/verify-account', methods=['GET', 'POST'])
@login_required
def verify_request():
  try:
    if request.method == 'POST':
      user_id = current_user.id
      firstname = request.form.get('firstname')
      lastname = request.form.get('lastname')
      gender = request.form.get('gender')
      day = request.form.get('birthday')
      month = request.form.get('birthmonth')
      year = request.form.get('birthyear')
      birthday = f"{year}-{month}-{day}"
      address = request.form.get('address')
      mailAddress = request.form.get('mailAddress')
      contactnum = request.form.get('contactnum')
      id_upload = request.files.get('id_upload') 
      id_type = request.form.get('id_type')
      id_number = request.form.get('id_number')

      if 'id_upload' in request.files:
        if id_upload.filename != '':
          allowed_extensions = {'png', 'jpg', 'jpeg'}
          if '.' in id_upload.filename and id_upload.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            # print(f"Cloud Name: {cloudinary.config().cloud_name}")
            # print(f"API Key: {cloudinary.config().api_key}")
            # print(f"API Secret: {cloudinary.config().api_secret}")
            # result = cloudinary.uploader.upload(id_upload)
            # result_url = result["secure_url"]

            url = "https://api.imgbb.com/1/upload"
            imgbb_api_key = '9d6ce6cd8c83495edc23596db1eda476'
            params = {"key": imgbb_api_key}
            response = requests.post(url, files={'image': id_upload}, params=params)      
            id_url = response.json()
            if 'data' in id_url and 'url' in id_url['data']:
                result_url = id_url['data']['url']
            else:
                flash('Failed to retrieve image URL from ImgBB API response.', 'danger')
                return redirect(request.url)

            user = User.userData1(user_id)
            if user:
              User_Verification_Data.updateVerify_Data(user_id, firstname, lastname, gender, birthday, address, mailAddress, contactnum, result_url, id_type, id_number)              
            else:            
              User_Verification_Data.addVerify_Data(user_id, firstname, lastname, gender, birthday, address, mailAddress, contactnum, result_url, id_type, id_number)
            user_name = user[0][1]
            user_id = user[0][0]
            user = User(user_id)
            session['loggedin']= True
            session['username']= user_name
            session['user_id']= user_id
            login_user(user, remember=True)
            flash('We are currently verifying your account!', 'success')
            #return jsonify({'success': True, 'message': 'We are currently verifying your account!'})
            return redirect(url_for('home.home_page')) 
          else:
              flash('Invalid file format. Allowed formats are png, jpg, jpeg', 'danger')
              return redirect(request.url)
            
      flash('File not found in the request.', 'danger')
      return redirect(request.url)
  
  except Exception as e:
    print(f"Error during verification: {str(e)}")
    
  return render_template("request-verify.html", user=current_user)