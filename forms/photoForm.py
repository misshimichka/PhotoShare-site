from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class PhotoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('Info', validators=[DataRequired()])
    image = FileField("Choose file")
    submit = SubmitField('Save changes')
