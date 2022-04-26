from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField('О себе', validators=[DataRequired()])
    image = FileField("Выберите файл")
    submit = SubmitField('Изменить')