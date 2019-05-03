from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.projects.models import Project
from application.projects.tasks.models import Task
from application.projects.categories.models import Category
from application.projects.forms import ProjectForm
from application.auth.models import User

@app.route("/projects/", methods=["GET"])
@login_required
def projects_list():
    projects = current_user.projects
    return render_template("projects/list.html", projects = projects)

@app.route("/projects/", methods=["POST"])
@login_required
def projects_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("projects/new.html", form = form)

    new_project = Project(form.name.data, form.deadline.data, current_user.id)

    db.session().add(new_project)
    db.session().commit()

    current_user.add_project(new_project.id)

    return redirect(url_for("projects_list"))

@app.route("/projects/new/")
@login_required
def projects_form():
    return render_template("projects/new.html", form = ProjectForm())

@app.route("/projects/<project_id>/", methods=["GET"])
@login_required
def projects_view(project_id):
    project = Project.query.get(project_id)
    
    if project.has_access(current_user.id):
        tasks = Task.query.filter_by(project_id = project.id)
        categories = Category.query.filter_by(project_id = project.id)
        creator = User.query.get(project.creator)
        contributors = project.accounts

        return render_template("projects/view.html", project = project, tasks = tasks, categories = categories, creator_name = creator.name, contributors = contributors)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/edit/", methods=["GET"])
@login_required
def projects_edit_form(project_id):
    project = Project.query.get(project_id)

    if project.has_access(current_user.id):
        return render_template("projects/edit.html", project = project, form = ProjectForm())
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/confirm_delete/", methods=["GET"])
@login_required
def projects_confirm_delete(project_id):
    project = Project.query.get(project_id)

    if project.creator == current_user.id:
        task_count = Task.query.filter_by(project_id = project.id).count()
        category_count = Category.query.filter_by(project_id = project.id).count()

        return render_template("projects/confirm_delete.html", project = project, task_count = task_count, category_count = category_count)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/delete/", methods=["GET"])
@login_required
def projects_delete(project_id):
    project = Project.query.get(project_id)

    if project.creator == current_user.id:
        Task.query.filter_by(project_id = project.id).delete()
        Category.query.filter_by(project_id = project.id).delete()
        Project.query.filter_by(id = project_id).delete()

        db.session().commit()

    return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/", methods=["POST"])
@login_required
def projects_edit(project_id):
    project = Project.query.get(project_id)

    if project.has_access(current_user.id):
        form = ProjectForm(request.form)

        if not form.validate():
            return render_template("projects/edit.html", project = project, form = form)

        project.name = form.name.data
        project.deadline = form.deadline.data

        db.session().commit()

    return redirect(url_for("projects_view", project_id = project.id))

@app.route("/projects/join/<invite_token>")
@login_required
def projects_join(invite_token):
    project = Project.query.filter_by(invite_token = invite_token).first()

    if project:
        if not project.has_access(current_user.id):
            current_user.add_project(project.id)

        return redirect(url_for("projects_view", project_id = project.id))
    else:
        return redirect(url_for("index"))

