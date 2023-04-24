import random
import re
import string
from datetime import datetime

from flask import url_for

from yacut import db

MAX_SHORT_ID_LENGTH = 16
PATTERN = r'[a-zA-Z0-9]'
SIMBOLS = string.ascii_letters + string.digits


class URLMap(db.Model):
    """Модель для связи оригинальной ссылки и короткого идентификатора."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'short_url_view',
                short=self.short,
                _external=True
            )
        )

    def from_dict(self, data, short_id):
        self.original = data['url']
        self.short = short_id


def short_id_is_valid(short_id):
    if len(short_id) > MAX_SHORT_ID_LENGTH:
        return False
    checked_short_id = [
        letter for letter in short_id if re.match(PATTERN, letter)
    ]
    if len(short_id) != len(checked_short_id):
        return False
    return True


def short_id_is_exist(short_id):
    return URLMap.query.filter_by(short=short_id).first() is not None


def get_unique_short_id():
    short_id = ''.join(random.choices(SIMBOLS, k=6))
    return get_unique_short_id() if short_id_is_exist(short_id) else short_id
