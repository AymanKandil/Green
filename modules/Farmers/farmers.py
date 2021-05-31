from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required, current_user
from modules.Auth.user_db import UserDatabase
from models import requires_access_level


farmer = Blueprint(
    'farmer', __name__
)

@farmer.route("/")
@login_required
def farmer_view():                                          #userprofile view
    db = UserDatabase(current_app.config["USERS_DB"])
    loggeduser = current_user.get_id()  
    data = db.get_logged_farmer(loggeduser)                 #Retrieves current logged user information from the database
    chars = []
    for i in data:                                          #Using a nested for loop to assign the retrieved data into an array instead of tuble
        for c in i:
            chars.append(c)
        
    fname = chars[1]                            #Takes the first name from array
    lname = chars[2]                            #Takes last name from array
    fname1 = fname[0]                           #Takes first char from firstname
    lname1 = lname[0]                           #Takes first char from last name
    return render_template("user-profile.html", variable=data, fnamein=fname1, lnamein=lname1)
