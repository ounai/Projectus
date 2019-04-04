from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.projects.models import Project, Task
from application.projects.forms import ProjectForm, TaskForm

@app.route("/projects/", methods=["GET"])
@login_required
def projects_list():
    return render_template("projects/list.html", projects = Project.query.filter_by(account_id = current_user.id))

@app.route("/projects/", methods=["POST"])
@login_required
def projects_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("projects/new.html", form = form)

    new_project = Project(form.name.data)
    new_project.account_id = current_user.id
    new_project.deadline = form.deadline.data

    db.session().add(new_project)
    db.session().commit()

    return redirect(url_for("projects_list"))

@app.route("/projects/new/")
@login_required
def projects_form():
    return render_template("projects/new.html", form = ProjectForm())

@app.route("/projects/<project_id>/", methods=["GET"])
@login_required
def projects_view(project_id):
    project = Project.query.get(project_id)
    
    if project.account_id == current_user.id:
        tasks = Task.query.filter_by(project_id = project.id)
        task_count = tasks.count()

        return render_template("projects/view.html", project = project, tasks = tasks, task_count = task_count)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/", methods=["POST"])
@login_required
def projects_edit(project_id):
    project = Project.query.get(project_id)

    if project.account_id == current_user.id:
        if request.form.get("name") != "":
            project.name = request.form.get("name")

        db.session().commit()

    return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/new_task/", methods=["GET"])
@login_required
def tasks_form(project_id):
    project = Project.query.get(project_id)

    if project.account_id == current_user.id:
        return render_template("projects/new_task.html", form = TaskForm(), project = project)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/new_task/", methods=["POST"])
@login_required
def tasks_create(project_id):
    project = Project.query.get(project_id)

    if project.account_id == current_user.id:
        form = TaskForm(request.form)

        if not form.validate():
            return render_template("projects/new_task.html", form = form)

        new_task = Task(form.name.data)
        new_task.project_id = project_id
        new_task.deadline = form.deadline.data

        db.session().add(new_task)
        db.session().commit()

    return redirect(url_for("projects_view", project_id = project_id))

