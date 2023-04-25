from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional

ORIGINAL_LINK = 'Добавьте исходную ссылку'
CUSTOM_ID = 'Добавьте свой вариант короткой ссылки'
SUBMIT = 'Создать'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK,
        validators=[Length(1, 256)]
    )
    custom_id = URLField(
        CUSTOM_ID,
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField(
        SUBMIT
    )
