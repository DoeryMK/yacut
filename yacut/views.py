from flask import abort, flash, redirect, render_template, url_for

from settings import SHORT_URL_VIEW
from yacut import app
from yacut.error_handlers import (INVALID_SHORT_ID, FailedShortIdValidation,
                                  ShortIdIsNotFound, ShortIdIsNotUnique)
from yacut.forms import URLForm
from yacut.models import URLMap

SHORT_ID_IS_EXIST = 'Имя {short_id} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция для главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_id = form.custom_id.data
    try:
        urlmap = URLMap.create(
            original=form.original_link.data,
            short=short_id,
        )
        short_id = url_for(
            SHORT_URL_VIEW,
            short=urlmap.short,
            _external=True
        )
        return render_template(
            'index.html', form=form, short_id=short_id
        )
    except FailedShortIdValidation:
        flash(
            INVALID_SHORT_ID
        )
        return render_template(
            'index.html', form=form
        )
    except ShortIdIsNotUnique:
        flash(
            SHORT_ID_IS_EXIST.format(short_id=short_id)
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
    except ShortIdIsNotFound:
        abort(404)
