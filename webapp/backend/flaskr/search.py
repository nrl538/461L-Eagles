from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import functools

from flaskr.db import get_db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        search_param = request.form['q']
        cur = get_db().cursor()
        error = None

        cur.execute(
            'SELECT * FROM books WHERE books.title LIKE %s', ('%' + search_param + '%',)
        )

        books_by_title = cur.fetchall()

        cur.execute(
            'SELECT * FROM books WHERE books.author LIKE %s', ('%' + search_param + '%',)
        )

        books_by_author = cur.fetchall()

        if books_by_title is None and books_by_author is None:
            error = 'No Books were found'
            return error
        flash(error)

        books = books_by_author + books_by_title
    return render_template('books/results.html', books=books)
