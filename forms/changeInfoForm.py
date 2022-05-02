from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    about = TextAreaField('About', validators=[DataRequired()])
    image = FileField("Choose file")
    submit = SubmitField('Save changes')