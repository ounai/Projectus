from application import db
from application.models import Base

from sqlalchemy.sql import text

class Project(Base):
    name = db.Column(db.String(144), nullable = False)
    complete = db.Column(db.Boolean, nullable = False)
    deadline = db.Column(db.Date, nullable = False)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)

    tasks = db.relationship("Task", backref = "project_task", lazy = True)
    categories = db.relationship("Category", backref = "category", lazy = True)

    def __init__(self, name, deadline, account_id):
        self.name = name
        self.complete = False
        self.deadline = deadline
        self.account_id = account_id

    @staticmethod
    def find_projects_by_user_with_tasks_due_on(account_id, deadline):
        stmt = text("SELECT Project.id, Project.name FROM Project"
                    " LEFT JOIN Task on Task.project_id = Project.id"
                    " WHERE (Task.deadline = :deadline AND Project.account_id = :account_id AND NOT Task.complete)"
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

