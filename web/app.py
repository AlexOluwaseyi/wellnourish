#!/usr/bin/python3
"""
Web View of the WellNourish App
This is where all interactions with the web browser starts from

This is also the entry point of the application
"""
from models import storage
from models.user import User
from flask import Flask, render_template, redirect, url_for, request
from flask_login import (LoginManager, UserMixin, login_user,
                         current_user, login_required, logout_user)
from uuid import uuid4


app = Flask(__name__)


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
    return render_template("login.html", title="Login")


@app.route("/register", strict_slashes=False, methods=['GET', 'POST'])
@app.route("/register.html", strict_slashes=False, methods=['GET', 'POST'])
def register():
    """WellNourish Registration Route"""
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Create a new user and save it to the database here
        new_user = User(username=username, email=email, password=password)
        storage.add(new_user)
        storage.save()
        # Redirect to profile setup page
        return redirect(url_for('profile_setup'))
    return render_template("register.html", title="Register")


@app.route('/completeprofile', strict_slashes=False, methods=['GET', 'POST'])
def complete_profile():
    """WellNourish Profile Setup Route
    Add more information to the User model"""
    if request.method == 'POST':
        # Handle form submission
        current_user.fname = request.form['fname']
        current_user.lname = request.form['lname']
        current_user.healthrecords = request.form.getlist('healthrecords')
        # Create a new user and save it to the database here
        storage.save()
        # Redirect to profile setup page
        return redirect(url_for('profile'))
    return render_template('profile_setup.html', title="Complete Profile")


@app.route('/resetpassword')
def resetpass():
    """WellNourish Profile Setup Route"""
    return render_template('reset_password.html', title="Reset Password")


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
