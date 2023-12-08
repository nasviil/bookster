from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.userprofilemodel import UserProfile  
from flask_login import current_user

userprofile = Blueprint('userprofile', __name__)

def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.id
    else:
        return None
    
@userprofile.route('/userprofile', methods=['GET'])
def user_profile():
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Fetch user profile data
    user_profile_data = UserProfile.get_user_profile(user_id)
    return render_template('userprofile.html', user_profile_data=user_profile_data,username=username)


@userprofile.route('/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile_route(user_id):
    user_profile_data = UserProfile.get_user_profile(user_id)

    if user_profile_data:
        return render_template('userprofile.html', user_profile_data=user_profile_data)
    else:
        return render_template('userprofile.html', message='User profile not found'), 404
    
    

@userprofile.route('/edituserprofile', methods=['GET', 'POST'])
def edit_user_profile():
    if request.method == 'POST':
        # Handle the form submission
        user_id = session.get('user_id')

        # Fetch user profile data
        user_profile_data = UserProfile.get_user_profile(user_id)

        # Update user profile information based on the form submission
        UserProfile.update_user_profile(
            user_id,
            request.form['name'],
            request.form['bio'],
            request.form['facebook'],
            request.form['instagram'],
            request.form['twitter']
        )

        flash('Profile updated successfully', 'success')

        return redirect(url_for('userprofile.user_profile'))

    elif request.method == 'GET':
        # Handle the GET request, maybe render the form
        user_id = session.get('user_id')

        # Fetch user profile data
        user_profile_data = UserProfile.get_user_profile(user_id)

        return render_template('edituserprofile.html', user_profile_data=user_profile_data)