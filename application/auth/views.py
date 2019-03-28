from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login/", methods=["GET"])
def auth_login_form():
    return render_template("auth/login_form.html", form = LoginForm())

@app.route("/auth/login/", methods=["POST"])
def auth_login():
    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()

    if not user:
        return render_template("auth/login_form.html", form = form, error = "Incorrect username or password")

    print("User " + user.name + " has logged in")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods=["GET"])
def auth_register_form():
    return render_template("auth/register_form.html", form = RegisterForm())

@app.route("/auth/register", methods=["POST"])
def auth_register():
    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/register_form.html", form = form)

    if User.query.filter_by(username=form.username.data).first():
        return render_template("auth/register_form.html", form = form, error = "Username already in use")

    new_user = User(form.name.data, form.username.data, form.password.data)

    db.session().add(new_user)
    db.session().commit()

    login_user(new_user)
    return redirect(url_for("index"))

