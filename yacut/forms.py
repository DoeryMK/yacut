from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (
    InputRequired, Length, Optional,
    Regexp, ValidationError
)

from settings import (
    MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LENGTH,
    SHORT_PATTERN
)
from yacut.error_handlers import INVALID_SHORT
from yacut.models import URLMap

ORIGINAL_LINK_COMMENT = 'Добавьте исходную ссылку'
CUSTOM_ID_COMMENT = 'Добавьте свой вариант короткой ссылки'
SHORT_IS_EXIST = 'Имя {short} уже занято!'
SUBMIT_COMMENT = 'Создать'
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
                max=MAX_SHORT_LENGTH,
                message=INVALID_SHORT
            ),
            Optional(),
            Regexp(
                regex=SHORT_PATTERN,
                message=INVALID_SHORT
            )
        ]
    )
    submit = SubmitField(
        SUBMIT_COMMENT
    )

    def validate_custom_id(flaskform, field):
        if URLMap.get(field.data):
            raise ValidationError(
                SHORT_IS_EXIST.format(
                    short=field.data
                )
            )
