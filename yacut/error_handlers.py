from flask import jsonify, render_template

from yacut import app, db

INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
FAILED_AUTO_GENERATION = "Ошибка автоматической генерации short_id"
NO_REQUEST_BODY = 'Отсутствует тело запроса'
SHORT_ID_NOT_FOUND = 'Указанный id не найден'
URL_IS_REQUIRED = '\"url\" является обязательным полем!'


class FailedShortIdAutoGeneration(Exception):
    """Ошибка автоматической генерации short_id."""
    pass


class FailedShortIdValidation(Exception):
    """Ошибка валидации: недопустимый short_id."""
    pass


class ShortIdIsNotUnique(Exception):
    """Ошибка проверки на уникальность: short_id существует."""
    pass


class ShortIdIsNotFound(Exception):
    """Указанный short_id не найден."""
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
