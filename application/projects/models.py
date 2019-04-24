from random import randint

from application import db
from application.models import Base

from application.auth.models import UserProject

from sqlalchemy.sql import text

class Project(Base):
    name = db.Column(db.String(144), nullable = False)
    complete = db.Column(db.Boolean, nullable = False)
    deadline = db.Column(db.Date, nullable = False)
    invite_token = db.Column(db.Integer, nullable = False)

    creator = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    accounts = db.relationship('User', secondary = "user_project")

    tasks = db.relationship("Task", backref = "project_task", lazy = True)
    categories = db.relationship("Category", backref = "category", lazy = True)

    def __init__(self, name, deadline, creator):
        self.name = name
        self.complete = False
        self.deadline = deadline
        self.creator = creator
        self.invite_token = randint(1000000000, 9999999999)

    def has_access(self, account_id):
        user_project = UserProject.query.filter_by(account_id = account_id, project_id = self.id)
        return user_project.count() >= 1

    @staticmethod
    def find_projects_by_user_with_tasks_due_on(account_id, deadline):
        stmt = text("SELECT Project.id, Project.name FROM Project"
                    " LEFT JOIN Task on Task.project_id = Project.id"
                    " WHERE (Task.deadline = :deadline AND Project.creator = :account_id AND NOT Task.complete)"
                    " GROUP BY Project.id").params(deadline = deadline, account_id = account_id)

        res = db.engine.execute(stmt)

        result = []
        for row in res:
            result.append({
                "id": row[0],
                "name": row[1]
            })

        return result

class Task(Base):
    name = db.Column(db.String(144), nullable = False)
    complete = db.Column(db.Boolean, nullable = False)
    deadline = db.Column(db.Date, nullable = False)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable = False)
    
    def __init__(self, name, deadline, project_id, category_id):
        self.name = name
        self.complete = False
        self.deadline = deadline

        self.project_id = project_id
        self.category_id = category_id

class Category(Base):
    name = db.Column(db.String(144), nullable = False)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)

    tasks = db.relationship("Task", backref = "category_task", lazy = True)

    def __init__(self, name, project_id):
        self.name = name

        self.project_id = project_id

