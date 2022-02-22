from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Job title', validators=[DataRequired()])
    team_leader_id = StringField('Team Leader ID')
    work_size = StringField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators')
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')