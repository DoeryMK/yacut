import random
import re
from datetime import datetime

from flask import url_for

from settings import (ALLOWED_SIMBOLS, AUTO_SHORT_LENGTH,
                      MAX_GET_AUTO_ATTEMPT_NUMBER, MAX_ORIGINAL_LINK_LENGTH,
                      MAX_SHORT_LENGTH, SHORT_PATTERN, SHORT_URL_ENDPOINT)
from yacut import db
from yacut.error_handlers import (FAILED_AUTO_GENERATION,
                                  FailedShortAutoGeneration,
                                  FailedShortValidation, ShortIsNotFound,
                                  ShortIsNotUnique)


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
    def get_original_url(short):
        urlmap = URLMap.query.filter_by(short=short).first()
        if urlmap is None:
            raise ShortIsNotFound
        return urlmap.original

    @staticmethod
    def create(original, short):
        if short == '' or short is None:
            short = URLMap.get_unique_short()
        else:
            short = URLMap.short_is_valid(short)
            if URLMap.short_is_exist(short):
                raise ShortIsNotUnique
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
            raise FailedShortValidation
        if re.fullmatch(
                pattern=SHORT_PATTERN,
                string=short,
                flags=re.ASCII
        ) is None:
            raise FailedShortValidation
        return short

    @staticmethod
    def short_is_exist(short):
        return URLMap.query.filter_by(short=short).first() is not None

    @staticmethod
    def get_unique_short():
        counter = 1
        while True:
            short = ''.join(random.choices(
                ALLOWED_SIMBOLS,
                k=AUTO_SHORT_LENGTH
            ))
            if not URLMap.short_is_exist(short):
                return short
            counter += 1
            if counter >= MAX_GET_AUTO_ATTEMPT_NUMBER:
                raise FailedShortAutoGeneration(
                    FAILED_AUTO_GENERATION
                )
