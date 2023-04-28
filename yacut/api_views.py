from flask import jsonify, request

from yacut import app
from yacut.error_handlers import (INVALID_SHORT, NO_REQUEST_BODY,
                                  SHORT_NOT_FOUND, URL_IS_REQUIRED,
                                  FailedShortValidation, InvalidAPIUsage,
                                  ShortIsNotFound, ShortIsNotUnique)
from yacut.models import URLMap

SHORT_IS_EXIST = 'Имя "{short}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    """Обработка запроса на создание короткой ссылки."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_IS_REQUIRED)
    short = data.get('custom_id') if 'custom_id' in data else None
    try:
        urlmap = URLMap.create(
            original=data['url'],
            short=short,
        )
        return jsonify(urlmap.to_dict()), 201
    except FailedShortValidation:
        raise InvalidAPIUsage(
            INVALID_SHORT
        )
    except ShortIsNotUnique:
        raise InvalidAPIUsage(
            SHORT_IS_EXIST.format(short=short)
        )


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Обработка запроса на получение оригинальной ссылки."""
    try:
        return jsonify({'url': URLMap.get_original_url(short)}), 200
    except ShortIsNotFound:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND, 404
        )
