from flask import jsonify, render_template

from yacut import app, db

INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
FAILED_AUTO_GENERATION = 'Ошибка автоматической генерации идентификатора'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
SHORT_IS_TOO_LONG = (
    'Размер короткого идентификатора превышен. '
    'Допустимое количество символов равно {length}.'
)
SHORT_NOT_FOUND = 'Указанный id не найден'
SHORT_NOT_UNIQUE = 'Имя {short} уже занято!'
URL_IS_REQUIRED = '\"url\" является обязательным полем!'
URL_IS_TOO_LONG = (
    'Размер оригинальной ссылки превышен. '
    'Допустимое количество символов равно {length}.'
)


class FailedShortAutoGeneration(Exception):
    """Ошибка автоматической генерации короткого идентификатора."""
    pass


class FailedShortValidation(Exception):
    """Ошибка валидации: недопустимый короткий идентификатор."""
    pass


class ShortIsNotUnique(Exception):
    """Ошибка проверки на уникальность: короткий идентификатор существует."""
    pass


class ShortIsNotFound(Exception):
    """Указанный короткий идентификатор не найден."""
    pass


class FailedOriginalValidation(Exception):
    """Ошибка валидации: превышен размер оригинальной ссылки."""
    pass


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
