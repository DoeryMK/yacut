from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import (URLMap, get_unique_short_id, short_id_is_exist,
                          short_id_is_valid)

CONTENT_TYPE = 'application/json'


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    content_type = request.headers.get('Content-Type')
    if content_type != CONTENT_TYPE:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    short_id = data['custom_id'] if 'custom_id' in data else None
    if short_id == '' or short_id is None:
        short_id = get_unique_short_id()
    else:
        if not short_id_is_valid(short_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if short_id_is_exist(short_id):
            raise InvalidAPIUsage(
                f'Имя "{short_id}" уже занято.'
            )
    url = URLMap()
    url.from_dict(data, short_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is not None:
        return jsonify({'url': url.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
