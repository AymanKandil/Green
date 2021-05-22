from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required, current_user
from modules.Auth.user_db import UserDatabase
from models import requires_access_level


user = Blueprint(
    'user', __name__
)



@user.route("/")
@login_required
@requires_access_level([1])
def user_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    roles = db.get_roles()
    users = db.get_users()
    users_sorted = {}
    for user in users:
        current_user= {}
        # current_user = users_sorted.get(user[1], {
        #     "roles": []
        # })
        current_user["id"] = user[0]
        current_user["name"] = user[1]
        current_user["role"]= db.check_role_id(user[6])

        # if not user[3]:
        #     current_user["roles"].append(["No role", "None", "999"])
        # else:
        #     current_user["roles"].append([user[6], user[7], user[8]])
        users_sorted[user[1]] = current_user
    return render_template("user.html", roles=roles, users=users_sorted)

@user.route("/role/add", methods=["POST"])
@login_required
@requires_access_level([1])
def role_add_post():
    name = request.form.get("name")
    db = UserDatabase(current_app.config["USERS_DB"])
    if not name:
        flash("No name supplied", "error")
        return render_template("user.html")
    db.insert_role(name)
    flash("Role name successfully added", "success")
    return redirect(url_for("user.user_view"))

@user.route("/role/<user>/add", methods=["POST"])
@login_required
@requires_access_level([1])
def role_add_user_post(user):
    name = request.form.get("roles")
    db = UserDatabase(current_app.config["USERS_DB"])
    if not name:
        flash("No name supplied", "error")
        return render_template("user.html")
    user_id = db.check_user(user)[2]
    role_id = db.check_role(name)[0]
    
    # if not user_id or not role_id:
    #     flash("Incorrect user or role", "error")
    #     return redirect(url_for("user.user_view"))

    # if db.check_user_id(user_id):
    #     flash("{} already has the role {}".format(user, name), "error")
    #     return redirect(url_for("user.user_view"))

    # db.insert_user_role(user_id, role_id)
    # flash("Successfully added role to user", "success")
    db.update_role_id(role_id, user_id)
    return redirect(url_for("user.user_view"))

@user.route("/<user>/remove", methods=["POST"])
@login_required
@requires_access_level([1])
def remove_user_post(user):
    db = UserDatabase(current_app.config["USERS_DB"])
    db.remove_user(user)
    return redirect(url_for("user.user_view"))