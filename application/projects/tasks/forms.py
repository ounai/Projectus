from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.fields.html5 import DateField

class TaskForm(FlaskForm):
    name = StringField("Task name", [validators.Length(min = 3, max = 144)])
    deadline = DateField("Deadline")

    class Meta:
        csrf = False
