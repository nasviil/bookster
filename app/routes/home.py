from flask import Blueprint, render_template
from flask_login import login_required


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home_page():
    return render_template("homepage.html")


