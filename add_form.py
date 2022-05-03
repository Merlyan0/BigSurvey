from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddingSurveyForm(FlaskForm):
    """
    Форма создание опроса.
    """
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание (необязательно)')
    ask_name = BooleanField('Запрашивать ФИ пользователя, проходящего опрос')
    private = BooleanField('Приватный опрос (Будет доступен только по особой ссылке)')
    password = PasswordField('Пароль для будущего редактирования опроса и просмотра результатов',
                             validators=[DataRequired()])
    submit = SubmitField('Сохранить')
