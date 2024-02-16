#!/usr/bin/python3
"""
Web View of the WellNourish App
This is where all interactions with the web browser starts from

This is also the entry point of the application
"""

from models import storage
from models.user import User
from flask import (Flask, flash, render_template, session,
                   redirect, url_for, request, abort, flash)
from flask_login import (LoginManager, current_user, login_user,
                         login_required, logout_user)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellnourish.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


"""Declaration of diets and intolerances (allergies)
FUll list of diets and intolerances as specified by spoonacular
Diets - https://spoonacular.com/food-api/docs#Diets
Intolerances - https://spoonacular.com/food-api/docs#Intolerances
"""
diets = ['Gluten Free', 'Ketogenic', 'Vegetarian',
         'Lacto-Vegetarian', 'Ovo-Vegetarian',
         'Vegan', 'Pescetarian', 'Paleo', 'Primal',
         'Low FODMAP', 'Whole30']

intolerances = ['Dairy', 'Egg', 'Gluten', 'Grain', 'Peanut',
                'Seafood', 'Sesame', 'Shellfish', 'Soy',
                'Sulfite', 'Tree Nut', 'Wheat']


@login_manager.user_loader
def load_user(user_id):
    """Your implementation to load a user
    from the database using the id"""
    return storage.get(User, user_id)


@app.route("/", strict_slashes=False)
def index():
    """WellNourish Index Route"""
    return render_template("index.html", title="Home")


@app.route("/about", strict_slashes=False)
def about():
    """WellNourish About Route"""
    return render_template("about.html", title="About")


@app.route("/logout", strict_slashes=False)
def logout():
    """WellNourish Logout User Route"""
    logout_user()
    return redirect(url_for('index'))


@app.route("/login", strict_slashes=False, methods=['GET', 'POST'])
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
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Create a new user and save it to the database here
        new_user = User(username=username, email=email,
                        password=password)

        try:
            storage.new(new_user)
            storage.save()

        except IntegrityError as E:
            """Handle integrity constraint violation
            (e.g., username or email already exists)"""
            flash('Username or email already exists')
            return redirect(url_for('register'))

        if new_user.check_password(password):
            login_user(new_user)
            # Redirect to profile setup page
            return redirect(url_for('complete_profile', user_id=new_user.id))

    return render_template("register.html", title="Register")


@app.route('/completeprofile/<user_id>', methods=['GET', 'POST'])
def complete_profile(user_id):
    """WellNourish Profile Setup Route
    Add more information to the User model"""
    current_user = storage.get(User, user_id)
    if request.method == 'POST':
        # Handle form submission
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.gender = request.form['gender']
        current_user.intolerances = request.form.getlist('selectedIntolerances')
        current_user.diets = request.form.getlist('selectedDiets')
        # Create a new user and save it to the database here
        storage.save()
        # Redirect to profile setup page
        return redirect(url_for('profile'))
    return render_template('profile_setup.html', title="Complete Profile",
                           diets=diets, intolerances=intolerances)


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpass():
    """WellNourish Profile Setup Route"""
    return render_template('reset_password.html', title="Reset Password")


@app.route('/profile')
def profile():
    return render_template('index.html', user=current_user)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
