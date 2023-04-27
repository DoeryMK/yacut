import random
import re
from datetime import datetime

from flask import url_for

from settings import (ALLOWED_SIMBOLS, AUTO_SHORT_ID_LENGTH,
                      MAX_GET_AUTO_ATTEMPT_NUMBER, MAX_ORIGINAL_LINK_LENGTH,
                      MAX_SHORT_ID_LENGTH, SHORT_ID_PATTERN, SHORT_URL_VIEW)
from yacut import db
from yacut.error_handlers import (FAILED_AUTO_GENERATION,
                                  FAILED_SHORT_ID_VALIDATION,
                                  FailedShortIdAutoGeneration,
                                  FailedShortIdValidation)


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
        db.String(MAX_SHORT_ID_LENGTH),
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
            short_link=url_for(
                SHORT_URL_VIEW,
                short=self.short,
                _external=True
            )
        )

    @staticmethod
    def create(original, short):
        urlmap = URLMap(
            original=original,
            short=short,
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def get_original_url(short):
        urlmap = URLMap.query.filter_by(short=short).first()
        return urlmap.original if urlmap is not None else None

    @staticmethod
    def short_id_is_valid(short_id):
        """
        Как-то обрабатывать ошибки
        """
        if len(short_id) > MAX_SHORT_ID_LENGTH:
            # raise FailedShortIdValidation(FAILED_SHORT_ID_VALIDATION)
            return False
        if re.fullmatch(
                pattern=SHORT_ID_PATTERN, string=short_id, flags=re.ASCII
        ) is None:
            # raise FailedShortIdValidation(FAILED_SHORT_ID_VALIDATION)
            return False
        return short_id

    @staticmethod
    def short_id_is_exist(short_id):
        return URLMap.query.filter_by(short=short_id).first() is not None

    @staticmethod
    def get_unique_short_id():
        """
        Как-то обрабатывать ошибки
        """
        counter = 1
        while True:
            short_id = ''.join(
                random.choices(ALLOWED_SIMBOLS, k=AUTO_SHORT_ID_LENGTH))
            if not URLMap.short_id_is_exist(short_id):
                return short_id
            counter += 1
            if counter >= MAX_GET_AUTO_ATTEMPT_NUMBER:
                raise FailedShortIdAutoGeneration(FAILED_AUTO_GENERATION)
