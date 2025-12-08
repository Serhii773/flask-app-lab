from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Ім'я є обов'язковим."),
            Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів."),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email є обов'язковим."),
            Email(message="Введіть коректну адресу email."),
        ],
    )

    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Телефон є обов'язковим."),
            Regexp(
                r"^\+380\d{9}$",
                message="Телефон повинен бути у форматі +380XXXXXXXXX.",
            ),
        ],
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("support", "Support"),
            ("bug", "Bug report"),
            ("offer", "Cooperation offer"),
            ("other", "Other"),
        ],
        validators=[DataRequired(message="Оберіть тему повідомлення.")],
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Повідомлення є обов'язковим."),
            Length(
                max=500,
                message="Довжина повідомлення не повинна перевищувати 500 символів.",
            ),
        ],
    )

    submit = SubmitField("Send")


class LoginForm(FlaskForm):
    username = StringField(
        "Username / Email",
        validators=[DataRequired(message="Ім'я користувача або email є обов'язковим.")],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Пароль є обов'язковим."),
            Length(
                min=4,
                max=10,
                message="Пароль має бути довжиною від 4 до 10 символів.",
            ),
        ],
    )

    remember = BooleanField("Remember me")

    submit = SubmitField("Sign In")
