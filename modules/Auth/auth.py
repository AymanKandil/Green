from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import re
from modules.Auth.user_db import UserDatabase
from models import User



auth = Blueprint(
    'auth', __name__)


@auth.route("/login")
def login():
    if current_user.is_authenticated: ##Uses inbuilt Flask library to check if user is currently logged in and directs them to selected HTML file
        return redirect(url_for("farmer.farmer_view"))
    return render_template("login.html")

@auth.route("/login", methods=["POST"])                     #Login method. Takes the username and password from the form and checks it against database
def login_post():                                           #Compares password with hashed version of password if correct will login user if not will flash and error message
    username = request.form.get("username")
    password = request.form.get("password")
    db = UserDatabase(current_app.config["USERS_DB"])
    user = db.check_user(username)
    if user:
        if check_password_hash(user[1], password):
            user = User(user[0])
            login_user(user)
            return redirect(url_for("index"))
    flash("Incorrect username or password", "error")
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["POST", "GET"])                       #Register method takes inputed values from form and inserts them to the database
def register_post():                                                    #Passwords hashed before entering database
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    confirm_password = request.form.get("confirm_password")

    db = UserDatabase(current_app.config["USERS_DB"])


    # Validate username
    if not re.match("^[a-zA-z0-9]{2,10}$", username):                   #Checks username in database and makes sure it fits the critera set.
        flash("Inavlid username.", "error")
        return redirect(url_for("auth.register_view"))

    # Valid password
    if not (password_check(password).get("password_ok", False)):                    #Checks password and makes sure it meets conditions
        # flash("Your password is not strong enough, make sure it meets"
        #       "the following requirements:", "error")
        # flash("8 or more characters", "error")
        # flash("1 or more lowercase letters", "error")
        # flash("1 or more uppercase letters", "error")
        # flash("1 or more special characters", "error")
        # flash("1 or more digits", "error")
        return redirect(url_for("auth.register_post"))
    if confirm_password != password:                                            #Checks password matches confirm password
        # flash("Passwords do not match", "error")
        return redirect(url_for("auth.register_post"))

    user = db.check_user(username)

    # Check if user exists
    if user:                                                            #Checks if username already exists in database
        # flash("Username already taken", "error")
        return redirect(url_for("auth.register_post"))

    # Register user
    db.insert_user(username, first_name, last_name, email, generate_password_hash(password, method="sha256") )  #The command to insert user into database. Passwords are using Sha256 encryption
    # flash("You were successfully registered, please log in", "success")
    return redirect(url_for("auth.login"))

@auth.route("/logout")                          # Logout method uses Flask_login manager innate logout method
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def password_check(password):
    """
    Source: https://stackoverflow.com/a/32542964/6340707
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(
        r"[ ?@!#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password
    ) is None

    # overall result
    password_ok = not (
        length_error or digit_error or uppercase_error or
        lowercase_error or symbol_error
    )

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
