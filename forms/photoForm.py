from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class PhotoForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    about = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField("Выберите файл")
    submit = SubmitField('Добавить')
