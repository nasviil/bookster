from flask import Blueprint, render_template, session
from app.models.userprofilemodel import UserProfile  # Add this import
from flask_login import current_user

userprofile = Blueprint('userprofile', __name__)

def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.id
    else:
        # Handle the case where the user is not authenticated
        return None
    
@userprofile.route('/userprofile', methods=['GET'])
def user_profile():
    # Assuming you have a function to get the current user ID, adjust this accordingly
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Fetch user profile data
    user_profile_data = UserProfile.get_user_profile(user_id)
    return render_template('userprofile.html', user_profile_data=user_profile_data,username=username)

# Example usage in a route
@userprofile.route('/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile_route(user_id):
    user_profile_data = UserProfile.get_user_profile(user_id)

    if user_profile_data:
        return render_template('userprofile.html', user_profile_data=user_profile_data)
    else:
        return render_template('userprofile.html', message='User profile not found'), 404
    
@userprofile.route('/edituserprofile')
def edit_user_profile():
    return render_template('edituserprofile.html')