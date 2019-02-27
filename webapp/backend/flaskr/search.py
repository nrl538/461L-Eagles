# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:01:05 2019

@author: Doly
"""
import functools
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

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

        flash(error)
    return render_template('books/results.html')