# -*- coding: utf-8 -*-
import functools
import math

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
        perpage=3
        startat=(page-1)*perpage
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
        search_type=request.form.get("type")
        if search_type==None:
            search_type="None"
        f=open("C:\\Users\\Doly\\Desktop/debug.txt","w")
        f.write(search_type)
        if search_type=="1":
            books=books_by_title
        elif search_type=="2":
            books=books_by_author
        else:
            books = books_by_author + books_by_title
        total=int(math.ceil((len(books)/perpage)/2))
        if total==0:
            total=1
        books = books[0:3]
        
        #pagination = Pagination(page=page, pagination=pagination,total=users.count(),  record_name='books')

        
    elif request.method == 'GET':
        perpage=3
        search_param=request.args.get("q")
        
        if search_param==None:
            search_param=""
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
        if books_by_title is None and books_by_author is None:
            error = 'No Books were found'
            return error
        flash(error)
        search_type=str(request.args.get("search_type"))
        if search_type==None:
            search_type="None"
        f=open("C:\\Users\\Doly\\Desktop/debug.txt","w")
        f.write(search_type)
        if search_type=="1":
            books=books_by_title
        elif search_type=="2":
            books=books_by_author
        else:
            books = books_by_author + books_by_title

    return render_template('book/results.html',total=total,books=books,page=page,search_param=search_param,search_type=search_type)



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
