from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Enter title"),
            Length(max=150, message="Maximum 150 characters"),
        ],
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired(message="Enter the text of the post")],
    )

    enabled = BooleanField(
        "Active post",
        default=True,
    )

    publish_date = DateTimeLocalField(
        "Publish date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.utcnow,
        validators=[DataRequired(message="Please indicate the date and time of publication")],
    )

    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Tech"),
            ("other", "Other"),
        ],
        validators=[DataRequired(message="Select a category")],
    )

    submit = SubmitField("Submit")


class DeletePostForm(FlaskForm):
    submit = SubmitField("Delete")
