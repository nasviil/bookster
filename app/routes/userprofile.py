from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
import cloudinary.uploader
from app.models.userprofilemodel import UserProfile
from flask import current_app

userprofile = Blueprint('userprofile', __name__)

# Add your Cloudinary configuration here
cloudinary.config(
    cloud_name='dclxaugvd',
    api_key='412149475729753',
    api_secret='VJNHyUvJEUXrrH2uAmfQDhIUIRk'
)

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
    
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

@userprofile.route('/edituserprofile', methods=['GET', 'POST'])
def edit_user_profile():
    user_id = get_current_user_id()  # Ensure user_id is defined

    if request.method == 'POST':
        # Fetch user profile data
        user_profile_data = UserProfile.get_user_profile(user_id)

        # Check if a new profile picture is uploaded
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']

            # Check if a file is selected
            if profile_picture and allowed_file(profile_picture.filename):
                # Continue with the Cloudinary upload process
                cloudinary_response = cloudinary.uploader.upload(profile_picture)
                cloudinary_url = cloudinary_response.get('secure_url')

                # Update user profile information with the Cloudinary URL
                UserProfile.update_user_profile(
                    user_id,
                    request.form['name'],
                    cloudinary_url,
                    request.form['bio'],
                    request.form['facebook'],
                    request.form['instagram'],
                    request.form['twitter']
                )

                flash('Profile updated successfully', 'success')

                return redirect(url_for('userprofile.user_profile'))  # Redirect to user_profile route

        # If no new profile picture is uploaded or an invalid file is selected,
        # update without changing the image
        UserProfile.update_user_profile(
            user_id,
            request.form['name'],
            user_profile_data.image_url,
            request.form['bio'],
            request.form['facebook'],
            request.form['instagram'],
            request.form['twitter']
        )

        flash('Profile updated successfully', 'success')

        return redirect(url_for('userprofile.user_profile'))  # Redirect to user_profile route

    elif request.method == 'GET':
        # Fetch user profile data
        user_profile_data = UserProfile.get_user_profile(user_id)
        return render_template('edituserprofile.html', user_profile_data=user_profile_data)

    # Add a default return statement in case none of the conditions are met
    return "Invalid request"
