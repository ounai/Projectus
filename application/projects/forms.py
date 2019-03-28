from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ProjectForm(FlaskForm):
    name = StringField("Project name", [validators.Length(min=3)])

    class Meta:
        csrf = False
