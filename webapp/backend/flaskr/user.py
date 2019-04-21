import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET'])
def show():
    if session['user_id']:
        cursor = get_db().cursor()
        return get_my_books(cursor)
    else:
        flash("Please login first.")
        return redirect('/login')

def get_recently_viewed_query():
    query = "select * from users "\
            "left outer join recently_viewed "\
            "on users.id = recently_viewed.user_id "\
            "right outer join books "\
            "on books.id = recently_viewed.book_id "\
            "where users.id = %s"
    return query

def get_saved_books_query():
    query = "select * from users "\
            "left outer join saved_books "\
            "on users.id = saved_books.user_id "\
            "where user.id = %s"
    return query

def carouselify(books):
    books_per_slide = 5

    if len(books) < books_per_slide:
        carousel_books = [books] # list of lists
        return carousel_books
    else:
        carousel_books = []
        number_sub_lists = len(books) // books_per_slide

        for i in range(number_sub_lists):
            carousel_books.append([])

        carousel_slide_number = 0
        num_seen = 0
        for i in range(len(books)):
            # select the current carousel slide #
            if num_seen % books_per_slide == 0 and num_seen != 0:
                carousel_slide_number += 1

            print(carousel_slide_number)
            carousel_books[carousel_slide_number].append(books[i])
            num_seen += 1
        return carousel_books




def get_my_books(cursor):
    cursor.execute(get_recently_viewed_query(), (session['user_id'],))
    recently_viewed = carouselify(cursor.fetchall())
    return render_template('user/profile.html', recently_viewed=recently_viewed)

