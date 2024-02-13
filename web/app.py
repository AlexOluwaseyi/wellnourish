#!/usr/bin/python3
"""
Web View of the WellNourish App
This is where all interactions with the web browser starts from

This is also the entry point of the application
"""

from models import storage
from models.user import User
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import (LoginManager, UserMixin, login_user,
                         current_user, login_required, logout_user)
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellnourish.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Your implementation to load a user from the database using the user_id
    return User.query.get(int(user_id))


@app.route("/", strict_slashes=False)
def index():
    """WellNourish Index Route"""
    return render_template("index.html", title="Home")


@app.route("/about", strict_slashes=False)
def about():
    """WellNourish About Route"""
    return render_template("about.html", title="About")


@app.route("/login", strict_slashes=False)
def login():
    """WellNourish User Login Route"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template("login.html", title="Login")


@app.route("/register", strict_slashes=False, methods=['GET', 'POST'])
def register():
    """WellNourish Registration Route"""
    if request.method == 'POST':
        # Handle form submission
        id = uuid4()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = None
        last_name = None
        # Create a new user and save it to the database here
        new_user = User(id=id, username=username, email=email,
                        password=password, first_name=first_name,
                        last_name=last_name)
        storage.new(new_user)
        storage.save()
        # Redirect to profile setup page
        return redirect(url_for('complete_profile'))
    return render_template("register.html", title="Register")


@app.route('/completeprofile', strict_slashes=False, methods=['GET', 'POST'])
def complete_profile():
    """WellNourish Profile Setup Route
    Add more information to the User model"""
    if request.method == 'POST':
        # Handle form submission
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.health_records = request.form.getlist('health_records')
        current_user.allergies = request.form.getlist('allergies')
        # Create a new user and save it to the database here
        storage.save()
        # Redirect to profile setup page
        return redirect(url_for('profile'))
    return render_template('profile_setup.html', title="Complete Profile")


@app.route('/resetpassword')
@login_required
def resetpass():
    """WellNourish Profile Setup Route"""
    return render_template('reset_password.html', title="Reset Password")


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
