from flask import current_app, redirect, url_for
from modules.Auth.user_db import UserDatabase
from functools import wraps
from flask_login import current_user, AnonymousUserMixin

ACCESS = {
    'Guest': 3,
    'user': 2,
    'admin': 1
}

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.allowed(access_level):
                return redirect(url_for("dashboard.dashboard_view"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class User():
    def __init__(self, user_id):
        self.user_id = user_id

        db = UserDatabase(current_app.config["USERS_DB"])
        user_data = db.check_user(self.user_id)
        self.id = user_data[2]
        self.username = user_data[0]
        self.access = user_data[3]
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def is_admin(self):
        return self.access == ACCESS['admin']

 

    def allowed(self, access_level):
        
        if self.access ==access_level[0]:
            return True
        else:
            return False

    def __unicode__(self):
        return self.user_id
        
class Anonymous(AnonymousUserMixin):
    '''
    This is the default object for representing an anonymous user.
    '''
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return
    
    def __init__(self):
        self.username = "Guest"
        self.access= 3

    def allowed(self, access_level):

        if self.access == access_level[0]:
           
            return True
        else:
         
            return False
        
