from flask import abort, flash, redirect, render_template, url_for

from settings import SHORT_URL_VIEW
from yacut import app, db
from yacut.error_handlers import INVALID_SHORT_ID
from yacut.forms import URLForm
# SHORT_ID_IS_EXIST = 'Имя {short_id} уже занято!'
from yacut.models import URLMap

# from yacut.models import (URLMap, get_unique_short_id, short_id_is_exist,
#                           short_id_is_valid)



@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция для главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_id = form.custom_id.data
    if short_id == '' or short_id is None:
        short_id = URLMap.get_unique_short_id()
    # else:
    #     if not short_id_is_valid(short_id):
    #         flash(INVALID_SHORT_ID)
    #         return render_template('index.html', form=form, url=None)
    #     if short_id_is_exist(short_id):
    #         flash(SHORT_ID_IS_EXIST.format(short_id=short_id))
    #         return render_template('index.html', form=form, url=None)
    # url = URLMap(
    #     original=form.original_link.data,
    #     short=short_id,
    # )
    # db.session.add(url)
    # db.session.commit()
    urlmap = URLMap.create(
        original=form.original_link.data,
        short=short_id,
    )
    short_id = url_for(
        SHORT_URL_VIEW,
        short=urlmap.short,
        _external=True
    )
    return render_template('index.html', form=form, short_id=short_id)


@app.route('/<string:short>', methods=['GET'])
def short_url_view(short):
    """View-функция отвечающая за переадресацию."""
    # url = URLMap.query.filter_by(short=short).first()
    # if urlmap is None:
    #     abort(404)
    # return redirect(urlmap.original, code=302)
    original = URLMap.get_original_url(short)
    if original is None:
        abort(404)
    return redirect(original, code=302)
