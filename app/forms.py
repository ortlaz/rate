from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


# Форма регистрации


class SignUpForm(FlaskForm):
    name = StringField("ФИО", validators=[DataRequired(), Length(max=200)])
    email = StringField("Электронная почта", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль не должен быть менее %(min)d символов."),
        ],
    )
    password_conf = PasswordField(
        "Подтверждение пароля",
        validators=[
            DataRequired(message="Обязательно для заполнения."),
            EqualTo("password", message="Пароли не совпадают."),
        ],
    )
    submit = SubmitField("Зарегистрироваться")

    # Проверка существования e-mail

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Адрес электронной почты уже занят.")


# Форма Авторизации


class SignInForm(FlaskForm):
    email = StringField("Электронная почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    # remember_me = BooleanField('Запомнить меня')
    submit = SubmitField("Войти")
