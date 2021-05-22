from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint(
    'dashboard', __name__
)

@dashboard.route("/")
@login_required
def dashboard_view():
    return render_template("dashboard.html")