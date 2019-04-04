from application import db
from application.models import Base

class Project(Base):
    name = db.Column(db.String(144), nullable = False)
    complete = db.Column(db.Boolean, nullable = False)
    deadline = db.Column(db.Date, nullable = False)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)

    def __init__(self, name):
        self.name = name
        self.complete = False

class Task(Base):
    name = db.Column(db.String(144), nullable = False)
    complete = db.Column(db.Boolean, nullable = False)
    deadline = db.Column(db.Date, nullable = False)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)
    
    def __init__(self, name):
        self.name = name
        self.complete = False

