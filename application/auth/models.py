from application import db
from application.models import Base

class User(Base):
    __tablename__ = "account"

    name = db.Column(db.String(144), nullable = False)
    username = db.Column(db.String(144), nullable = False)
    password = db.Column(db.String(144), nullable = False)

    own_projects = db.relationship("Project", backref = "account", lazy = True)
    projects = db.relationship("Project", secondary = "user_project")
    roles = db.relationship("Role", backref = "account", lazy = True)

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

    def add_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return

        role = Role(role_name, self.id)

        db.session().add(role)
        db.session().commit()

    def remove_role(self, role_name):
        if self.has_role(role_name):
            Role.query.filter_by(account_id = self.id, name = role_name).delete()
            db.session().commit()

    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True

        return False

class Role(Base):
    name = db.Column(db.String(144), nullable = False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))

    def __init__(self, name, account_id):
        self.name = name
        self.account_id = account_id

class UserProject(db.Model):
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), primary_key = True)

    def __init__(self, account_id, project_id):
        self.account_id = account_id
        self.project_id = project_id

