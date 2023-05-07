from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.error_handlers import (
    FAILED_AUTO_GENERATION, FailedShortAutoGeneration,
    ShortIsNotFound
)
from yacut.forms import URLForm
from yacut.models import URLMap


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
            validation_required=False,
        )
        return render_template(
            'index.html',
            form=form,
            short_link=urlmap.get_absolute_short_url()
        )
    except FailedShortAutoGeneration:
        flash(
            FAILED_AUTO_GENERATION
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
