#!/usr/bin/python3
"""
Web View of the WellNourish App
This is where all interactions with the web browser starts from

This is also the entry point of the application
"""

from creds import secretKey
from models import storage
from flask import (Flask, flash, render_template, session,
                   redirect, url_for, request, abort, flash)
from flask_login import (LoginManager, current_user, login_user,
                         login_required, logout_user)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json
from models.user import User
import requests


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellnourish.db'
app.config['SECRET_KEY'] = secretKey
# db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


"""Declaration of diets and intolerances (allergies)
FUll list of diets and intolerances as specified by spoonacular
Diets - https://spoonacular.com/food-api/docs#Diets
Intolerances - https://spoonacular.com/food-api/docs#Intolerances
"""
diets = ['Gluten-Free', 'Ketogenic', 'Vegetarian',
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
    if "_user_id" in session:
        u_diets = session['diet']
        u_intolerances = session['intolerances']
    else:
        u_diets = ""
        u_intolerances = ""
    diet = [x.lower() for x in diets]
    intolerance = [x.lower() for x in intolerances]

    return render_template("index.html", title="Home", diets=diet,
                           intolerances=intolerance, u_diets=u_diets,
                           u_intolerances=u_intolerances)


@app.route("/landing_page", strict_slashes=False)
def landing_page():
    """WellNourish Index Route"""
    return render_template("landing_page.html", title="Landing")


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
        user = storage.session.query(User).filter_by(username=username).first()
        if user:
            if user.username and user.check_password(password):
                user_id = user.id
                login_user(user)
                session['diet'] = ' '.join([x.lower() for x in json.loads(user.diets)]).replace(' ', ',')
                session['intolerances'] =' '.join([x.lower() for x in json.loads(user.intolerances)]).replace(' ', ',')
                return redirect(url_for('profile', user_id=user_id))
            else:
                flash('Password incorrect!')
        else:
            flash("Account does not exist, sign up now.")
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

        intolerances_list = request.form.get('intolerances_string').split(', ')
        diets_list = request.form.get('diets_string').split(', ')

        current_user.intolerances = json.dumps(intolerances_list)
        current_user.diets = json.dumps(diets_list)

        # Create a new user and save it to the database here
        storage.save()
        # Redirect to profile setup page
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('profile_setup.html', title="Complete Profile",
                           diets=diets, intolerances=intolerances)


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpass():
    """WellNourish Profile Setup Route"""
    return render_template('reset_password.html', title="Reset Password")


@app.route('/recipes/<recipe_id>', methods=['GET'], strict_slashes=False)
def recipe_profile(recipe_id):
    """WellNourish Recipe Details Route"""
    title = "Recipe Details"

    return render_template('recipe_detail.html', title=title,
                           recipe_id=recipe_id)


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    current_user = storage.get(User, user_id)
    # return render_template('index.html', user=current_user)
    if current_user.is_authenticated:
        if current_user.id == user_id:
            current_user = storage.get(User, user_id)
            return render_template('index.html', user=current_user)
        else:
            return "Unauthorized", 401  # Return unauthorized status code if user_id doesn't match current user's id
    else:
        return "Unauthorized", 401  # Return unauthorized status code if user is not logged in


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
