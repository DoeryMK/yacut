from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте исходную ссылку',
        validators=[Length(1, 256)]
    )
    custom_id = URLField(
        'Добавьте свой вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField(
        'Создать'
    )
