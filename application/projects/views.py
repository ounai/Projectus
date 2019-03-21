from application import app, db
from flask import redirect, render_template, request, url_for
from application.projects.models import Project

@app.route("/projects/", methods=["GET"])
def projects_list():
    return render_template("projects/list.html", projects = Project.query.all())

@app.route("/projects/", methods=["POST"])
def projects_create():
    new_project = Project(request.form.get("name"))

    db.session().add(new_project)
    db.session().commit()

    return redirect(url_for("projects_list"))

@app.route("/projects/new/")
def projects_form():
    return render_template("projects/new.html")

@app.route("/projects/<project_id>/", methods=["POST"])
def projects_edit():
    project = Project.query.get(project_id)

    if request.form.get("name") != "":
        project.name = request.form.name

    db.session().commit()

    return redirect(url_for("projects_list"))

