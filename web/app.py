#!/usr/bin/python3
"""
Web View of the WellNourish App
This is where all interactions with the web browser starts from

This is also the entry point of the application
"""
from models import storage
from models.user import User
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """WellNourish Index Route"""
    return render_template("index.html", title="Home")


@app.route("/about", strict_slashes=False)
def about():
    """WellNourish About Route"""
    return render_template("about.html", title="About")

@app.route("/register", strict_slashes=False, methods=['GET', 'POST'])
@app.route("/register.html", strict_slashes=False, methods=['GET', 'POST'])
def register():
    """WellNourish Registration Route"""
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Here you would typically save the user to the database
        # For simplicity, we'll just print the values
        print(f"Username: {username}, Email: {email}, Password: {password}")
        # Redirect to profile setup page
        return redirect(url_for('profile_setup'))
    return render_template("register.html", title="Register")

@app.route('/profile-setup')
def profile_setup():
    """WellNourish Profile Setup Route"""
    return render_template('profile_setup.html', title= "Complete Profile")


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5001)
    app.run(debug=True)
