from application import db
from application.models import Base

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
