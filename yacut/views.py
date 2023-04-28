from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.error_handlers import (
    INVALID_SHORT, FailedShortValidation, ShortIsNotFound,
    ShortIsNotUnique
)
from yacut.forms import URLForm
from yacut.models import URLMap

SHORT_IS_EXIST = 'Имя {short} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция для главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template(
            'index.html', form=form
        )
    short = form.custom_id.data
    try:
        urlmap = URLMap.create(
            original=form.original_link.data,
            short=short,
        )
        return render_template(
            'index.html',
            form=form,
            short_link=urlmap.get_absolute_short_url()
        )
    except FailedShortValidation:
        flash(
            INVALID_SHORT
        )
    except ShortIsNotUnique:
        flash(
            SHORT_IS_EXIST.format(short=short)
        )
    return render_template(
        'index.html', form=form
    )


@app.route('/<string:short>', methods=['GET'])
def short_url_view(short):
    """View-функция отвечающая за переадресацию."""
    try:
        return redirect(
            URLMap.get_original_url(short), code=302
        )
    except ShortIsNotFound:
        abort(404)
