import re

from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (InputRequired, Length, Optional, Regexp,
                                ValidationError)

from settings import (MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_ID_LENGTH,
                      SHORT_ID_PATTERN)
from yacut.error_handlers import INVALID_SHORT_ID
from yacut.models import short_id_is_exist

ORIGINAL_LINK_COMMENT = 'Добавьте исходную ссылку'
CUSTOM_ID_COMMENT = 'Добавьте свой вариант короткой ссылки'
SUBMIT_COMMENT = 'Создать'
SHORT_ID_IS_EXIST = 'Имя {short_id} уже занято!'
URL_IS_REQUIRED = 'Необходимо ввести исходную ссылку'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_COMMENT,
        validators=[
            Length(
                max=MAX_ORIGINAL_LINK_LENGTH
            ),
            InputRequired(
                message=URL_IS_REQUIRED
            )
        ]
    )
    custom_id = URLField(
        CUSTOM_ID_COMMENT,
        validators=[
            Length(
                max=MAX_SHORT_ID_LENGTH,
                message=INVALID_SHORT_ID
            ),
            Optional(),
            Regexp(
                regex=SHORT_ID_PATTERN,
                flags=re.ASCII,
                message=INVALID_SHORT_ID
            )
        ]
    )
    submit = SubmitField(
        SUBMIT_COMMENT
    )

    def validate_custom_id(flaskform, field):
        if short_id_is_exist(field.data):
            raise ValidationError(
                SHORT_ID_IS_EXIST.format(short_id=field.data)
            )
