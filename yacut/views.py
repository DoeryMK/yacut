from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.error_handlers import INVALID_SHORT_ID
from yacut.forms import URLForm
from yacut.models import (URLMap, get_unique_short_id, short_id_is_exist,
                          short_id_is_valid)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция для главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form, url=None)
    short_id = form.custom_id.data
    if short_id == '' or short_id is None:
        short_id = get_unique_short_id()
    # else:
    #     if not short_id_is_valid(short_id):
    #         flash(INVALID_SHORT_ID)
    #         return render_template('index.html', form=form, url=None)
        # if short_id_is_exist(short_id):
        #     flash(SHORT_ID_IS_EXIST.format(short_id=short_id))
        #     return render_template('index.html', form=form, url=None)
    url = URLMap(
        original=form.original_link.data,
        short=short_id,
    )
    db.session.add(url)
    db.session.commit()
    return render_template('index.html', form=form, url=url)


@app.route('/<string:short>', methods=['GET'])
def short_url_view(short):
    """View-функция отвечающая за переадресацию."""
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        abort(404)
    return redirect(url.original, code=302)
