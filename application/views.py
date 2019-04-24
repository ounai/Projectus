from flask import render_template
from flask_login import current_user

from datetime import date

from application import app
from application.projects.models import Project, Task

@app.route("/")
def index():
    if current_user.is_authenticated:
        today_date = date.today()

        projects_due_today = Project.query.filter_by(creator = current_user.id, complete = False, deadline = today_date)
        projects_with_tasks_due_today = Project.find_projects_by_user_with_tasks_due_on(current_user.id, today_date)

        return render_template("index.html", projects_due_today = projects_due_today, projects_with_tasks_due_today = projects_with_tasks_due_today)
    else:
        return render_template("index.html")

