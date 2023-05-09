import random
import re
from datetime import datetime

from flask import url_for

from settings import (
    ALLOWED_SIMBOLS, AUTO_SHORT_LENGTH,
    MAX_GET_AUTO_ATTEMPT_NUMBER, MAX_ORIGINAL_LINK_LENGTH,
    MAX_SHORT_LENGTH, SHORT_PATTERN, SHORT_URL_ENDPOINT
)
from yacut import db
from yacut.error_handlers import (
    FAILED_AUTO_GENERATION, INVALID_SHORT, SHORT_IS_TOO_LONG,
    SHORT_NOT_FOUND, SHORT_NOT_UNIQUE, URL_IS_TOO_LONG,
    FailedOriginalValidation, FailedShortAutoGeneration,
    FailedShortValidation, ShortIsNotFound,
    ShortIsNotUnique
)


class URLMap(db.Model):
    """Модель для связи оригинальной ссылки и короткого идентификатора."""
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(MAX_ORIGINAL_LINK_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(MAX_SHORT_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_absolute_short_url()
        )

    def get_absolute_short_url(self):
        return url_for(
            SHORT_URL_ENDPOINT,
            short=self.short,
            _external=True
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_original_url(short):
        urlmap = URLMap.get(short)
        if not urlmap:
            raise ShortIsNotFound(
                SHORT_NOT_FOUND
            )
        return urlmap.original

    @staticmethod
    def create(original, short, validation_required):
        if validation_required and len(original) > MAX_ORIGINAL_LINK_LENGTH:
            raise FailedOriginalValidation(
                URL_IS_TOO_LONG.format(
                    length=MAX_ORIGINAL_LINK_LENGTH
                )
            )
        if short == '' or short is None:
            short = URLMap.get_unique_short()
        elif validation_required:
            short = URLMap.short_is_valid(short)
        urlmap = URLMap(
            original=original,
            short=short,
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def short_is_valid(short):
        if len(short) > MAX_SHORT_LENGTH:
            raise FailedShortValidation(
                SHORT_IS_TOO_LONG
            )
        if not re.match(
            pattern=SHORT_PATTERN,
            string=short,
        ):
            raise FailedShortValidation(
                INVALID_SHORT
            )
        if URLMap.get(short):
            raise ShortIsNotUnique(
                SHORT_NOT_UNIQUE.format(
                    short=short
                )
            )
        return short

    @staticmethod
    def get_unique_short():
        for attempt in range(MAX_GET_AUTO_ATTEMPT_NUMBER):
            short = ''.join(random.choices(
                ALLOWED_SIMBOLS,
                k=AUTO_SHORT_LENGTH
            ))
            if not URLMap.get(short):
                return short
        raise FailedShortAutoGeneration(
            FAILED_AUTO_GENERATION
        )
