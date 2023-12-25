from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
import cloudinary.uploader
from app.models.userprofilemodel import UserProfile
from flask import current_app
import cloudinary
from dotenv import load_dotenv
from os import getenv
from werkzeug.exceptions import abort
from ..models.user_book import UserBook
from ..models.models import User


userprofile = Blueprint('userprofile', __name__)

# Add your Cloudinary configuration here
def cloudinary_configuration(app):
    cloud_name = getenv('CLOUDINARY_CLOUD_NAME')
    api_key = getenv('CLOUDINARY_API_KEY')
    api_secret = getenv('CLOUDINARY_API_SECRET')

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
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
        current_user.id = int(current_user.id)

        purchased_books = UserBook.get_user_purchase(user_id)
        purchase_detail, seller = None, None
        if purchased_books is not None:
            purchase_detail = [UserBook.get_book_details(order['book_id']) for order in purchased_books]
            seller = [User.userData1(order['seller_id']) for order in purchased_books]

        rented_books = UserBook.get_user_rents(user_id)
        rent_detail, owner = None, None
        if rented_books is not None:
            rent_detail = [UserBook.get_book_details(order['book_id']) for order in rented_books]
            owner = [User.userData1(order['owner_id']) for order in rented_books]
        return render_template('userprofile.html', user_profile_data=user_profile_data,user_id=user_id, purchased_books=purchased_books, purchase_detail=purchase_detail, seller=seller, rented_books=rented_books, rent_detail=rent_detail, owner=owner)
    else:
        return render_template('userprofile.html', message='User profile not found'), 404
    
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

@userprofile.route('/edituserprofile', methods=['GET', 'POST'])
def edit_user_profile():
    user_id = get_current_user_id()  # Ensure user_id is defined

    if request.method == 'POST':
        # Handle the form submission
        user_id = session.get('user_id')
        # Fetch user profile data
        user_profile_data = UserProfile.get_user_profile(user_id)

        # Check if a new profile picture is uploaded
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']

            # Check if a file is selected
            if profile_picture:
                # Check if the file is allowed
                if allowed_file(profile_picture.filename):
                    # Check if the file size exceeds the limit (adjust the limit as needed)
                    if profile_picture.content_length > 2 * 1024 * 1024:  # 2 MB
                        flash('File size exceeds the limit (2 MB)', 'danger')
                        return redirect(request.url)

                    # Continue with the Cloudinary upload process
                    cloudinary_response = cloudinary.uploader.upload(profile_picture)
                    cloudinary_url = cloudinary_response.get('secure_url')

                    # Update user profile information with the Cloudinary URL
                    if user_profile_data:
                        UserProfile.update_user_profile(
                            user_id,
                            request.form['name'],
                            cloudinary_url,
                            request.form['bio'],
                            request.form['facebook'],
                            request.form['instagram'],
                            request.form['twitter']
                        )
                    else:
                        flash('User profile not found', 'danger')
                        return redirect(url_for('userprofile.get_user_profile_route', user_id=user_id))  # Redirect to user_profile route

                    flash('Profile updated successfully', 'success')
                    return redirect(url_for('userprofile.get_user_profile_route', user_id=user_id))  # Redirect to user_profile route

                else:
                    flash('Invalid file format. Please upload a JPEG or PNG file.', 'danger')
                    return redirect(request.url)

        # If no new profile picture is uploaded or an invalid file is selected,
        # update without changing the image
        if user_profile_data:
            UserProfile.update_user_profile(
                user_id,
                request.form['name'],
                user_profile_data.image_url,
                request.form['bio'],
                request.form['facebook'],
                request.form['instagram'],
                request.form['twitter']
            )
        else:
            flash('User profile not found', 'danger')
            return redirect(url_for('userprofile.get_user_profile_route', user_id=user_id))  # Redirect to user_profile route

        flash('Profile updated successfully', 'success')
        return redirect(url_for('userprofile.get_user_profile_route', user_id=user_id))  # Redirect to user_profile route

    elif request.method == 'GET':
        # Handle the GET request, maybe render the form
        user_id = session.get('user_id')
        # Fetch user profile data
        user_profile_data = UserProfile.get_user_profile(user_id)
        return render_template('edituserprofile.html', user_profile_data=user_profile_data)

    # Add a default return statement in case none of the conditions are met
    return render_template('edituserprofile.html')
