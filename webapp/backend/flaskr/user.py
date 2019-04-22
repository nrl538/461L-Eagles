import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['POST'])
def update():
    if session['user_id'] and request.method == 'POST':
        book_id = get_id_from_post_data(request.data)
        if book_id is not None:
            if command_is_remove(request.data):
                remove_book(book_id)
            else:
                save_book(book_id)
    else:
        flash("Please login first.")
        return redirect('/login')

@bp.route('/profile', methods=['GET'])
def show():
    if session['user_id']:
        cursor = get_db().cursor()
        return get_my_books(cursor)
    else:
        flash("Please login first.")
        return redirect('/login')

def get_id_from_post_data(post_data):
    stringified_data = post_data.decode('utf-8')
    print(stringified_data)
    if stringified_data is not None:
        data = stringified_data.replace('&','=').split("=")
        if len(data) >= 2:
            return data[1]
        else:
            return None
    else:
        return None

def command_is_remove(post_data):
    stringified_data = post_data.decode('utf-8')
    print(stringified_data)
    if stringified_data is not None:
        data = stringified_data.replace('&','=').split("=")
        if len(data) > 2:
            return True
        else:
            return False
    else:
        return False

def get_save_book_query():
    query = "insert into saved_books "\
            "(book_id, user_id) "\
            "values (%s, %s) "
    return query

def book_is_saved(book_id):
    cursor = get_db().cursor()
    cursor.execute("select * from saved_books where user_id = %s and book_id = %s", (session['user_id'], book_id,))
    result = cursor.fetchall()
    if result is not None and len(result) >= 1:
        return True
    else:
        return False

def remove_book(book_id):
    cursor = get_db().cursor()

    if not book_is_saved(book_id):
        return False
    else:
        cursor.execute("delete from saved_books where user_id = %s and book_id = %s", (session['user_id'], book_id,))
        get_db().commit()
        return True

def save_book(book_id):
    cursor = get_db().cursor()

    if not book_is_saved(book_id):
        cursor.execute(get_save_book_query(), (book_id, session['user_id'],))
        get_db().commit()
        return True
    else:
        return False

def get_recently_viewed_query():
    query = "select distinct(books.id), books.cover, "\
            "recently_viewed.user_id, users.id, "\
            "recently_viewed.book_id, recently_viewed.id from users "\
            "left outer join recently_viewed "\
            "on users.id = recently_viewed.user_id "\
            "right outer join books "\
            "on books.id = recently_viewed.book_id "\
            "where users.id = %s order by "\
            "recently_viewed.id desc limit 10"

    return query

def get_recently_viewed_books():
    if g.user and session['user_id']:
        cursor = get_db().cursor()
        cursor.execute(get_recently_viewed_query(), (session['user_id'],))
        return cursor.fetchall();

def get_saved_books_query():
    query = "select * from users "\
            "left outer join saved_books "\
            "on users.id = saved_books.user_id "\
            "right outer join books "\
            "on books.id = saved_books.book_id "\
            "where users.id = %s "\
            "order by saved_books.id desc"
    return query

def get_saved_books():
    if g.user and session['user_id']:
        cursor = get_db().cursor()
        cursor.execute(get_saved_books_query(), (session['user_id'],))
        return cursor.fetchall();

def get_my_books(cursor):
    cursor.execute(get_recently_viewed_query(), (session['user_id'],))
    recently_viewed = get_recently_viewed_books()
    saved_books = get_saved_books()
    return render_template('user/profile.html', recently_viewed=recently_viewed, saved_books=saved_books)

