# -*- coding: utf-8 -*-
import functools
import math
import urllib
from flask_paginate import Pagination, get_page_parameter

from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('search', __name__)

@bp.route('/search/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        page=1
        perpage=10
        startat=(page-1)*perpage
        search_param = request.form['q']
        if search_param==None or str(search_param).replace(" ","")=="":
            return render_template('index.html')
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
        cur.execute(
            'SELECT * FROM books WHERE books.isbn LIKE %s', ('%' + search_param + '%',)
        )
        books_by_isbn = cur.fetchall()
        cur.execute(
            'SELECT * FROM books WHERE books.isbn LIKE %s OR books.title LIKE %s OR books.author LIKE %s;', ('%' + search_param + '%','%' + search_param + '%','%' + search_param + '%',)
        )
        books_by_integrate = cur.fetchall()
        if books_by_title is None and books_by_author is None:
            error = 'No Books were found'
            return error
        flash(error)
        search_type=request.form.get("type")
        if search_type==None:
            search_type="None"
        
        if search_type=="1":
            books=books_by_title
        elif search_type=="2":
            books=books_by_author
        elif search_type=="3":
            books=books_by_isbn
        else:
            books=books_by_integrate
        total=int(math.ceil((len(books)/perpage)/2))
        if total==0:
            total=1
        books = books[0:perpage]
        
        #pagination = Pagination(page=page, pagination=pagination,total=users.count(),  record_name='books')

        
    elif request.method == 'GET':
        perpage=10
        search_param=request.args.get("q")
        
        if search_param==None:
            search_param=""
        search_param=urllib.unquote(search_param)

        page=int(request.args.get("page"))
        total=int(request.args.get("total"))
        if page>total:
            page=total
        if page==0:
            page=1
        startat=(page-1)*perpage
        cur = get_db().cursor()
        error = None 
        cur.execute(
            'SELECT * FROM books WHERE books.title LIKE %s LIMIT %s, %s;', ('%' + search_param + '%',startat,perpage,)
        )
        books_by_title = cur.fetchall()
        cur.execute(
            'SELECT * FROM books WHERE books.author LIKE %s LIMIT %s, %s;', ('%' + search_param + '%',startat,perpage,)
        )
        books_by_author = cur.fetchall()
        cur.execute(
            'SELECT * FROM books WHERE books.isbn LIKE %s LIMIT %s, %s;', ('%' + search_param + '%',startat,perpage,)
        )
        books_by_isbn = cur.fetchall()
        cur.execute(
                    'SELECT * FROM books WHERE books.isbn LIKE %s OR books.title LIKE %s OR books.author LIKE %s LIMIT %s, %s;', ('%' + search_param + '%','%' + search_param + '%','%' + search_param + '%',startat,perpage,)
            )
        books_by_integrate = cur.fetchall()
        if books_by_title is None and books_by_author is None:
            error = 'No Books were found'
            return error
        flash(error)
        search_type=str(request.args.get("search_type"))
        if search_type==None:
            search_type="None"
        
        
        if search_type=="1":
            books=books_by_title
        elif search_type=="2":
            books=books_by_author
        elif search_type=="3":
            books=books_by_isbn
        else:
            books=books_by_integrate
    search_param=urllib.quote(search_param)

    return render_template('book/results.html',total=total,books=books,page=page,search_param=search_param,search_type=search_type)



@bp.route('/search/names', methods=('GET', 'POST'))
def autocomplete():
    if request.method == 'GET':
        search_param = request.args.get('term')
        category = request.args.get('cat')
        cur = get_db().cursor()
        error = None
        if category == 'Title':
            return jsonify(matching_results=get_titles(cur, search_param))

        elif category == 'Author':
            return jsonify(matching_results=get_authors(cur, search_param))

        elif category == 'ISBN':
            return jsonify(matching_results=get_isbns(cur, search_param))

        aggregated = get_titles(cur, search_param) + get_authors(cur, search_param) + get_isbns(cur, search_param)
        return jsonify(matching_results=aggregated)

def get_titles(cur, search_param):
    cur.execute('SELECT DISTINCT TITLE FROM books WHERE books.title LIKE %s', ('%' + search_param + '%',))
    books_by_title = cur.fetchall()
    titles=[]
    for book_title in books_by_title:
        book = book_title['TITLE']
        if book != 'title':
            titles.append(book)

    return titles



def get_authors(cur, search_param):
    cur.execute('SELECT DISTINCT AUTHOR FROM books WHERE books.author LIKE %s', ('%' + search_param + '%',))
    books_by_author = cur.fetchall()
    authors = []
    for book_author in books_by_author:
        author = book_author['AUTHOR']
        if author != 'author':
            authors.append(author)
    
    return authors


def get_isbns(cur, search_param):
    cur.execute('SELECT DISTINCT ISBN FROM books WHERE books.isbn LIKE %s', ('%' + search_param + '%',))
    books_by_isbn = cur.fetchall()
    isbns = []
    for book_isbn in books_by_isbn:
        isbn = book_isbn['ISBN']
        if isbn != 'isbn':
            isbns.append(isbn)
    
    return isbns


