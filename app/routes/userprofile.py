from flask import Blueprint, render_template

userprofile = Blueprint('userprofile', __name__)

@userprofile.route('/userprofile')
def user_profile():
    return render_template('userprofile.html')

@userprofile.route('/edituserprofile')
def edit_user_profile():
    return render_template('edituserprofile.html')
