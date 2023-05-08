from flask import jsonify, request

from settings import MAX_ORIGINAL_LINK_LENGTH
from yacut import app
from yacut.error_handlers import (
    FAILED_AUTO_GENERATION, INVALID_SHORT, NO_REQUEST_BODY,
    SHORT_NOT_FOUND, URL_IS_REQUIRED, URL_IS_TOO_LONG,
    FailedOriginalValidation, FailedShortAutoGeneration,
    FailedShortValidation, InvalidAPIUsage, ShortIsNotFound,
    ShortIsNotUnique
)
from yacut.models import URLMap

SHORT_NOT_UNIQUE = 'Имя "{short}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    """Обработка запроса на создание короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            NO_REQUEST_BODY
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            URL_IS_REQUIRED
        )
    short = data.get('custom_id')
    try:
        return jsonify(
            URLMap.create(
                original=data['url'],
                short=short,
                validation_required=True,
            ).to_dict()
        ), 201
    except FailedOriginalValidation:
        raise InvalidAPIUsage(
            URL_IS_TOO_LONG.format(
                length=MAX_ORIGINAL_LINK_LENGTH
            )
        )
    except FailedShortAutoGeneration:
        raise InvalidAPIUsage(
            FAILED_AUTO_GENERATION
        )
    except FailedShortValidation:
        raise InvalidAPIUsage(
            INVALID_SHORT
        )
    except ShortIsNotUnique:
        raise InvalidAPIUsage(
            SHORT_NOT_UNIQUE.format(
                short=short
            )
        )


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Обработка запроса на получение оригинальной ссылки."""
    try:
        return jsonify(
            {'url': URLMap.get_original_url(short)}
        ), 200
    except ShortIsNotFound:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND, 404
        )
