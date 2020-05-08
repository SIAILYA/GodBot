from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class ManageForm(FlaskForm):
    title = StringField('Название')
    archived = BooleanField('Отображать в топе')
    auto_kick = BooleanField('Авто-кик')
    hello_msg = TextAreaField('Приветствие')
    submit = SubmitField('Сохранить')
