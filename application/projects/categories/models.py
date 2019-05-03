from application import db
from application.models import Base

class Category(Base):
    name = db.Column(db.String(144), nullable = False)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)

    tasks = db.relationship("Task", backref = "category_task", lazy = True)

    def __init__(self, name, project_id):
        self.name = name

        self.project_id = project_id