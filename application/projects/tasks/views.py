from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.projects.models import Project
from application.projects.tasks.models import Task
from application.projects.categories.models import Category
from application.projects.tasks.forms import TaskForm

@app.route("/projects/<project_id>/category/<category_id>/new_task/", methods=["GET"])
@login_required
def tasks_form(project_id, category_id):
    project = Project.query.get(project_id)
    category = Category.query.get(category_id)

    if project.has_access(current_user.id) and category.project_id == project.id:
        return render_template("projects/new_task.html", form = TaskForm(), project = project, category = category)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/category/<category_id>/new_task/", methods=["POST"])
@login_required
def tasks_create(project_id, category_id):
    project = Project.query.get(project_id)
    category = Category.query.get(category_id)

    if project.has_access(current_user.id) and category.project_id == project.id:
        form = TaskForm(request.form)

        if not form.validate():
            return render_template("projects/new_task.html", form = form, project = project, category = category)

        new_task = Task(form.name.data, form.deadline.data, project_id, category_id)

        db.session().add(new_task)
        db.session().commit()

    return redirect(url_for("projects_view", project_id = project_id))

@app.route("/projects/<project_id>/tasks/<task_id>/toggle_complete")
@login_required
def tasks_toggle_complete(project_id, task_id):
    project = Project.query.get(project_id)
    task = Task.query.get(task_id)

    if project.has_access(current_user.id) and task.project_id == project.id:
        task.complete = not task.complete

        db.session.commit()

    return redirect(url_for("projects_view", project_id = project_id))

@app.route("/projects/<project_id>/tasks/<task_id>/delete")
@login_required
def tasks_delete(project_id, task_id):
    project = Project.query.get(project_id)
    task = Task.query.get(task_id)

    if project.has_access(current_user.id) and task.project_id == project.id:
        Task.query.filter_by(id = task_id).delete()

        db.session.commit()

    return redirect(url_for("projects_view", project_id = project_id))

@app.route("/projects/<project_id>/tasks/<task_id>/edit/", methods=["GET"])
@login_required
def tasks_edit_form(project_id, task_id):
    project = Project.query.get(project_id)
    task = Task.query.get(task_id)

    if project.has_access(current_user.id) and task.project_id == project.id:
        return render_template("projects/edit_task.html", project = project, task = task, form = TaskForm())
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/tasks/<task_id>/edit/", methods=["POST"])
@login_required
def tasks_edit(project_id, task_id):
    project = Project.query.get(project_id)
    task = Task.query.get(task_id)

    if project.has_access(current_user.id) and task.project_id == project.id:
        form = TaskForm(request.form)

        if not form.validate():
            return render_template("projects/edit_task.html", project = project, task = task, form = form)

        task.name = form.name.data
        task.deadline = form.deadline.data

        db.session().commit()

    return redirect(url_for("projects_view", project_id = project_id))
