from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('book', __name__)

def get_book(isbn):
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * from books WHERE books.id = %s;', (isbn,)
    )
    book = cursor.fetchone()
    '''
    cursor.execute(
        'SELECT * from reviews WHERE reviews.id = %s;', (isbn,)
    )
    audience_review = cursor.fetchone()
    '''

    cursor.execute(
        'SELECT * FROM twitter WHERE twitter.id = %s;',(isbn,)
    )
    twitter_reviews = cursor.fetchall()
    for twitter_review in twitter_reviews:
        id_index = twitter_review['review_content'].find(str(isbn))
        twitter_review['review_content'] = twitter_review['review_content'][:id_index]

    cursor.execute(
        'SELECT * FROM amazon WHERE amazon.id = %s;', (isbn,)
    )
    amazon_reviews = cursor.fetchall()
    for a in amazon_reviews:
        print(a['review_content'])
    for amazon_review in amazon_reviews:
        id_index = amazon_review['review_content'].find(str(isbn))
        amazon_review['review_content'] = amazon_review['review_content'][:id_index]
    
    cursor.execute(
        'SELECT * FROM BN WHERE BN.id = %s;', (isbn,)
    )
    BN_reviews = cursor.fetchall()
    for b in BN_reviews:
        print(b['review_content'])
    for BN_review in BN_reviews:
        id_index = BN_review['review_content'].find(str(isbn))
        BN_review['review_content'] = BN_review['review_content'][:id_index]
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
    return render_template('book/book.html', book=book, review=all_reviews, sentiments=sentiments)

@bp.route('/book/<isbn>', methods=['GET'])
def show(isbn):
    book = get_book(isbn)
    return book
