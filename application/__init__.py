# Import Flask
from flask import Flask
app = Flask(__name__)

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# Import views
from application import views
from application.projects import views

# Import models
from application.projects import models

# Create db tables
db.create_all()

