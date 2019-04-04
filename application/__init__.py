# Import Flask
from flask import Flask
app = Flask(__name__, static_folder = "public", static_url_path = "")

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# DB config
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"
    app.config["SQLALCHEMY_ECHO"] = True

# Init DB
db = SQLAlchemy(app)

# Import views
from application import views
from application.projects import views
from application.auth import views

# Import models
from application.projects import models
from application.auth import models

# Login
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login_form"
login_manager.login_message = "Login required"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create db tables
try:
    db.create_all()
except:
    pass

