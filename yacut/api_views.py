from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import (INVALID_SHORT_ID, NO_REQUEST_BODY,
                                  SHORT_ID_NOT_FOUND, URL_IS_REQUIRED,
                                  InvalidAPIUsage)
# from yacut.models import (URLMap, get_unique_short_id, short_id_is_exist,
#                           short_id_is_valid)
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
    if short_id == '' or short_id is None:
        short_id = URLMap.get_unique_short_id()
    else:
        if not URLMap.short_id_is_valid(short_id):
            raise InvalidAPIUsage(INVALID_SHORT_ID)
        if URLMap.short_id_is_exist(short_id):
            raise InvalidAPIUsage(
                SHORT_ID_IS_EXIST.format(short_id=short_id)
            )
    # url = URLMap()
    # url.from_dict(data, short_id)
    # db.session.add(url)
    # db.session.commit()
    urlmap = URLMap.create(
        original=data['url'],
        short=short_id,
    )
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Обработка запроса на получение оригинальной ссылки."""
    # url = URLMap.query.filter_by(short=short).first()
    # if urlmap is not None:
    #     return jsonify({'url': urlmap.original}), 200
    # raise InvalidAPIUsage(SHORT_ID_NOT_FOUND, 404)
    original = URLMap.get_original_url(short)
    if original is None:
        raise InvalidAPIUsage(SHORT_ID_NOT_FOUND, 404)
    return jsonify({'url': original}), 200
