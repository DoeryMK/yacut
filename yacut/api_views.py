from flask import jsonify, request

from yacut import app
from yacut.error_handlers import (INVALID_SHORT_ID, NO_REQUEST_BODY,
                                  SHORT_ID_NOT_FOUND, URL_IS_REQUIRED,
                                  FailedShortIdValidation, InvalidAPIUsage,
                                  ShortIdIsNotFound, ShortIdIsNotUnique)
from yacut.models import URLMap

SHORT_ID_IS_EXIST = 'Имя "{short_id}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    """Обработка запроса на создание короткой ссылки."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_IS_REQUIRED)
    short_id = data.get('custom_id') if 'custom_id' in data else None
    try:
        urlmap = URLMap.create(
            original=data['url'],
            short=short_id,
        )
        return jsonify(urlmap.to_dict()), 201
    except FailedShortIdValidation:
        raise InvalidAPIUsage(
            INVALID_SHORT_ID
        )
    except ShortIdIsNotUnique:
        raise InvalidAPIUsage(
            SHORT_ID_IS_EXIST.format(short_id=short_id)
        )


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Обработка запроса на получение оригинальной ссылки."""
    try:
        return jsonify({'url': URLMap.get_original_url(short)}), 200
    except ShortIdIsNotFound:
        raise InvalidAPIUsage(
            SHORT_ID_NOT_FOUND, 404
        )
