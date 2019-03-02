from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import functools
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        title = request.form['title']
        cur = get_db().cursor()
        error = None
        cur.execute(
            'SELECT * FROM titles WHERE title LIKE %s', ('%'+title+'%',)
        )

        book=cur.fetchone()

        if book is None:
            error = 'No Books were found'
            return error

        flash(error)
    return render_template('book/results.html',books=[book])
