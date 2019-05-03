from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.projects.models import Project
from application.projects.categories.models import Category
from application.projects.tasks.models import Task
from application.projects.categories.forms import CategoryForm

@app.route("/projects/<project_id>/new_category", methods = ["GET"])
@login_required
def categories_form(project_id):
    project = Project.query.get(project_id)

    if project.has_access(current_user.id):
        return render_template("projects/new_category.html", form = CategoryForm(), project = project)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/new_category/", methods = ["POST"])
@login_required
def categories_create(project_id):
    project = Project.query.get(project_id)

    if project.has_access(current_user.id):
        form = CategoryForm(request.form)

        if not form.validate():
            return render_template("projects/new_category.html", form = form)

        new_category = Category(form.name.data, project_id)

        db.session().add(new_category)
        db.session().commit()

    return redirect(url_for("projects_view", project_id = project_id))

@app.route("/projects/<project_id>/category/<category_id>/confirm_delete/", methods=["GET"])
@login_required
def categories_confirm_delete(project_id, category_id):
    project = Project.query.get(project_id)
    category = Category.query.get(category_id)

    if project.has_access(current_user.id) and category.project_id == project.id:
        task_count = Task.query.filter_by(category_id = category.id).count()

        return render_template("projects/confirm_delete_category.html", project = project, category = category, task_count = task_count)
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/category/<category_id>/delete/", methods=["GET"])
@login_required
def categories_delete(project_id, category_id):
    project = Project.query.get(project_id)
    category = Category.query.get(category_id)

    if project.has_access(current_user.id) and category.project_id == project.id:
        Task.query.filter_by(category_id = category.id).delete()
        Category.query.filter_by(id = category.id).delete()

        db.session().commit()

    return redirect(url_for("projects_view", project_id = project.id))

@app.route("/projects/<project_id>/category/<category_id>/edit/", methods=["GET"])
@login_required
def categories_edit_form(project_id, category_id):
    project = Project.query.get(project_id)
    category = Category.query.get(category_id)

    if project.has_access(current_user.id) and category.project_id == project.id:
        return render_template("projects/edit_category.html", project = project, category = category, form = CategoryForm())
    else:
        return redirect(url_for("projects_list"))

@app.route("/projects/<project_id>/category/<category_id>/edit/", methods=["POST"])
@login_required
def categories_edit(project_id, category_id):
    project = Project.query.get(project_id)
    category = Category.query.get(category_id)

    if project.has_access(current_user.id) and category.project_id == project.id:
        form = CategoryForm(request.form)

        if not form.validate():
            return render_template("projects/edit_category.html", project = project, category = category, form = form)

        category.name = form.name.data

        db.session().commit()

    return redirect(url_for("projects_view", project_id = project_id))

