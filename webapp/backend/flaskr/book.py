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


    cursor.execute(
        'SELECT * from reviews WHERE reviews.id = %s', (isbn,)
    )
    review = cursor.fetchone()


    cursor.execute(
        'SELECT * from twitter WHERE twitter.id = %s', (isbn,)
    )
    twitter_review = cursor.fetchone()

    similar = similar(isbn)

    #initialize a dict to store all review sentiments
    #The key is the kind of review it is, and the value is a size 2 tuple representing the polarity and subjectivity
    all_reviews = {}

    review_sentiment = TextBlob(str(review['review_content'])).sentiment
    all_reviews['original_review'] = review_sentiment

    twitter_review_sentiment = TextBlob(str(twitter_review['review_content'])).sentiment
    all_reviews['twitter_review'] = twitter_review_sentiment

    return render_template('book/book.html', book=book, review=all_reviews, similar=similar)

# added functionality for returning array of book
def similar(id):
    cursor.execute(
        'SELECT * from similar WHERE similar.id = %s', (id,)
    )
    similar = cursor.fetchone()

    return [ret_book(similar['similar_1']),ret_book(similar['similar_2']),ret_book(similar['similar_3']),ret_book(similar['similar_4'])\
    ,ret_book(similar['similar_5'])]

# return the book based on id
def ret_book(id):
    cursor.execute(
        'SELECT * from books WHERE books.id = %s', (id,)
    )
    return cursor.fetchone()

@bp.route('/book/<isbn>', methods=['GET'])
def show(isbn):
    book = get_book(isbn)
    return book
