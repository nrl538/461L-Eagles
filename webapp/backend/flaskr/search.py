# -*- coding: utf-8 -*-
import functools

from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('search', __name__)

@bp.route('/search/', methods=('GET', 'POST'))
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
    return render_template('book/results.html', books=books)

@bp.route('/search/names', methods=('GET', 'POST'))
def autocomplete():
    if request.method == 'GET':
        search_param = request.args.get('term')
        category = request.args.get('cat')
        cur = get_db().cursor()
        error = None
        if category == 'Title':
            cur.execute(
                'SELECT TITLE FROM books WHERE books.title LIKE %s', ('%' + search_param + '%',)
            )

            books_by_title = cur.fetchall()
            titles=[]
            for book_title in books_by_title:
                book = book_title['TITLE']
                if book != 'title':
                    titles.append(book)

            return jsonify(matching_results=titles)

        elif category == 'Author':
            cur.execute(
                'SELECT AUTHOR FROM books WHERE books.author LIKE %s', ('%' + search_param + '%',)
            )

	    books_by_author = cur.fetchall()
            authors = []
            for book_author in books_by_author:
                author = book_author['AUTHOR']
                if author != 'author':
                    authors.append(author)

            return jsonify(matching_results=authors)

    return jsonify(matching_results=[])
