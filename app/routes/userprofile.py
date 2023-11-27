from flask import Blueprint, render_template

userprofile = Blueprint('userprofile', __name__)

@userprofile.route('/userprofile')
def user_profile():
    return render_template('userprofile.html')

# Example usage in a route
@userprofile.route('/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile_route(user_id):
    user_profile_data = UserProfile.get_user_profile(user_id)

    if user_profile_data:
        return render_template('profile.html', user_profile_data=user_profile_data)
    else:
        return render_template('profile.html', message='User profile not found'), 404
    
@userprofile.route('/edituserprofile')
def edit_user_profile():
    return render_template('edituserprofile.html')

from app.models.userprofilemodel import UserProfile

