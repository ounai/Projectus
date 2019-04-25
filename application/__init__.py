import os

# Import Flask
from flask import Flask
app = Flask(__name__, static_folder = "public", static_url_path = "")

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB config
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"
    app.config["SQLALCHEMY_ECHO"] = True

# Init DB
db = SQLAlchemy(app)

# Login
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login_form"
login_manager.login_message = "Login required"

# Authorization
from functools import wraps

def login_required(role = "ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True

                for user_role in current_user.roles:
                    if user_role.name == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Import views
from application import views
from application.projects import views
from application.auth import views

# Import models
from application.projects import models
from application.auth import models

from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create db tables
try:
    db.create_all()
except:
    pass

