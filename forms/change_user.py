from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    """ describe fields of change user form """
    name = StringField('Имя', validators=[DataRequired()])
    email = TextAreaField("Электронная почта")
    is_admin = BooleanField("Сделать Админом")
    submit = SubmitField('Применить')