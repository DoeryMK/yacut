from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional

from settings import MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_ID_LENGTH

ORIGINAL_LINK_COMMENT = 'Добавьте исходную ссылку'
CUSTOM_ID_COMMENT = 'Добавьте свой вариант короткой ссылки'
SUBMIT_COMMENT = 'Создать'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_COMMENT,
        validators=[Length(max=MAX_ORIGINAL_LINK_LENGTH)]
    )
    custom_id = URLField(
        CUSTOM_ID_COMMENT,
        validators=[Length(max=MAX_SHORT_ID_LENGTH), Optional()]
    )
    submit = SubmitField(
        SUBMIT_COMMENT
    )
