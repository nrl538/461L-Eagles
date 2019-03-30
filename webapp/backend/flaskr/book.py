from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('book', __name__)

def get_book(isbn):
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * from books WHERE books.id = %s', (isbn,)
    )
    book = cursor.fetchone()

    return render_template('book/book.html', book=book)

@bp.route('/book/<isbn>', methods=['GET'])
def show(isbn):
    book = get_book(isbn)
    return book
