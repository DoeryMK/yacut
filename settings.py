import os
import string

ALLOWED_SIMBOLS = string.ascii_letters + string.digits
AUTO_SHORT_LENGTH = 6
MAX_SHORT_LENGTH = 16
MAX_ORIGINAL_LINK_LENGTH = 2048
MAX_GET_AUTO_ATTEMPT_NUMBER = 256
SHORT_PATTERN = r'^[^\W_]+$'
SHORT_URL_ENDPOINT = 'short_url_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
