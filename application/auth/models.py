from application import db
from application.models import Base

class User(Base):
    __tablename__ = "account"

    name = db.Column(db.String(144), nullable = False)
    username = db.Column(db.String(144), nullable = False)
    password = db.Column(db.String(144), nullable = False)

    own_projects = db.relationship("Project", backref = "account", lazy = True)
    projects = db.relationship("Project", secondary = "user_project")

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def add_project(self, project_id):
        user_project = UserProject(self.id, project_id)

        db.session().add(user_project)
        db.session().commit()

class UserProject(db.Model):
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), primary_key = True)

    def __init__(self, account_id, project_id):
        self.account_id = account_id
        self.project_id = project_id

