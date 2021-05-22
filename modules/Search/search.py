from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required, current_user
from modules.Auth.user_db import UserDatabase
from models import requires_access_level
from modules.Farms.farms import farms

search = Blueprint(
    'search', __name__
)

@search.route("/", methods=['POST'])
def searchfield():
    db = UserDatabase(current_app.config["USERS_DB"])
    searchtext = request.form.get('searchtext')
    print(searchtext)
    return render_template(url_for('farms'))