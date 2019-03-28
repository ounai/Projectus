from flask import redirect, render_template, request, url_for

from application import app, db
from application.projects.models import Project
from application.projects.forms import ProjectForm

@app.route("/projects/", methods=["GET"])
def projects_list():
    return render_template("projects/list.html", projects = Project.query.all())

@app.route("/projects/", methods=["POST"])
def projects_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("projects/new.html", form = form)

    new_project = Project(form.name.data)

    db.session().add(new_project)
    db.session().commit()

    return redirect(url_for("projects_list"))

@app.route("/projects/new/")
def projects_form():
    return render_template("projects/new.html", form = ProjectForm())

@app.route("/projects/<project_id>/", methods=["GET"])
def projects_view(project_id):
    return render_template("projects/view.html", project = Project.query.get(project_id))

@app.route("/projects/<project_id>/", methods=["POST"])
def projects_edit(project_id):
    project = Project.query.get(project_id)

    if request.form.get("name") != "":
        project.name = request.form.get("name")

    db.session().commit()

    return redirect(url_for("projects_list"))

