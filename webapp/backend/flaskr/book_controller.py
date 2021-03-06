import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth_controller import login_required
from flaskr.db import get_db

# Import models
from flaskr.book import Book

bp = Blueprint('book', __name__)

def book_is_saved(book_id):
    if g.user and session['user_id']:
        cursor = get_db().cursor()
        cursor.execute("select * from saved_books where user_id = %s and book_id = %s", (session['user_id'], book_id,))
        result = cursor.fetchall()
        if result is not None and len(result) >= 1:
            return True
        else:
            return False
    else:
        return False 
# added functionality for returning array of book
def get_similar(id):
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * from similar WHERE similar.id = %s', (id,)
    )
    similar = cursor.fetchone()

    return [ret_book(similar['similar_1']),ret_book(similar['similar_2']),ret_book(similar['similar_3']),ret_book(similar['similar_4'])\
    ,ret_book(similar['similar_5'])]

# return the book based on id
def ret_book(id):
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * from books WHERE books.id = %s', (id,)
    )
    return cursor.fetchone()

def set_recently_viewed_books(isbn):
    if g.user and session['user_id']:
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

def get_book(isbn):
    similar = get_similar(isbn)

    cursor = get_db().cursor()

    book = Book.find(isbn)

    '''
    cursor.execute(
        'SELECT * from reviews WHERE reviews.book_id = %s;', (isbn,)
    )
    audience_review = cursor.fetchone()
    '''

    cursor.execute(
        'SELECT * FROM twitter WHERE twitter.book_id = %s;',(isbn,)
    )
    twitter_reviews = cursor.fetchall()
    
    cursor.execute(
        'SELECT * FROM amazon WHERE amazon.book_id = %s;', (isbn,)
    )
    amazon_reviews = cursor.fetchall()
    

    cursor.execute(
        'SELECT * FROM BN WHERE BN.book_id = %s;', (isbn,)
    )
    BN_reviews = cursor.fetchall()
    
        
    cursor.execute(
        'SELECT * FROM reddit WHERE reddit.book_id = %s;', (isbn,)
    )
    reddit_reviews = cursor.fetchall()
   
    #initialize a dict to store all review sentiments
    #The key is the kind of review it is, and the value is a size 2 tuple representing the polarity and subjectivity
    all_reviews = {}
    sentiments = {}
    '''
    review_sentiment = TextBlob(str(audience_review['review_content'])).sentiment
    all_reviews['audience_review'] = audience_review
    sentiments['audience_review'] = review_sentiment
    '''
    twitter_review_sentiments=[]
    for twitter_review in twitter_reviews:
        twitter_review_sentiment = TextBlob(str(twitter_review['review_content'])).sentiment
        twitter_review_sentiments.append(twitter_review_sentiment)
    all_reviews['twitter_review'] = twitter_reviews
    sentiments['twitter_review_sentiment'] = twitter_review_sentiments

    amazon_review_sentiments = []
    for amazon_review in amazon_reviews:
        amazon_review_sentiment = TextBlob(str(amazon_review['review_content'])).sentiment
        amazon_review_sentiments.append(amazon_review_sentiment)
    all_reviews['amazon_review'] = amazon_reviews
    sentiments['amazon_review_sentiment'] = amazon_review_sentiments

    BN_review_sentiments=[]
    for BN_review in BN_reviews:
        BN_review_sentiment = TextBlob(str(BN_review['review_content'])).sentiment
        BN_review_sentiments.append(BN_review_sentiment)
    all_reviews['BN_review'] = BN_reviews
    sentiments['BN_review_sentiment'] = BN_review_sentiments

    reddit_review_sentiments=[]
    for reddit_review in reddit_reviews:
        reddit_review_sentiment = TextBlob(str(reddit_review['review_content'])).sentiment
        reddit_review_sentiments.append(reddit_review_sentiment)
    all_reviews['reddit_review'] = reddit_reviews
    sentiments['reddit_review_sentiment'] = reddit_review_sentiments
    
    return render_template('book/book.html', book=book, review=all_reviews, sentiments=sentiments, similar=similar, saved=book_is_saved(book.id))


