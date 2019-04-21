from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
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

    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * from reviews WHERE reviews.id = %s', (isbn,)
    )
    review = cursor.fetchone()
    return render_template('book/book.html', book=book, review=review)

def set_recently_viewed_books(isbn):
    if session['user_id']:
        user_id = session['user_id']
        cursor = get_db().cursor()
        insert_query = "insert into recently_viewed (user_id, book_id) values (%s, %s)"
        cursor.execute(
            "insert into recently_viewed (user_id, book_id) values (%s, %s)", (user_id, isbn,)
        )
        get_db().commit()


@bp.route('/book/<isbn>', methods=['GET'])
def show(isbn):
    book = get_book(isbn)
    set_recently_viewed_books(isbn)
    return book
