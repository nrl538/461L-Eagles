# -*- coding: utf-8 -*-
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, Flask, current_app
)

from werkzeug.exceptions import abort
from textblob import TextBlob
from flaskr.auth_controller import login_required
from flaskr.db import get_db
from flaskr.model import Model

class Amazon_review(Model):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.id = dictionary["id"]
        self.book_id = dictionary["book_id"]
        self.title = dictionary["title"]
        self.isbn = dictionary["isbn"]
        self.author = dictionary["author"]
        self.review_source = dictionary["review_source"]
        self.average_rating = dictionary["average_rating"]
        self.review_author = dictionary["review_author"]
        self.review_content = dictionary["review_content"]
        
    @classmethod    
    def find_by_id(book_id):
        cursor = get_db().cursor()
        cursor.execute(
                'SELECT * FROM amazon WHERE amazon.book_id = %s;', (book_id,)
        )
        amazon_reviews_dictionary = cursor.fetchall()
        amazon_reviews = [];
        for amazon_review_dictionary in amazon_reviews_dictionary:
            amazon_review = Amazon_review(amazon_review_dictionary)
            amazon_reviews.append(amazon_review)
        return amazon_reviews
    
    @classmethod
    def find_by_isbn(isbn):
        cursor = get_db().cursor()
        cursor.execute(
                'SELECT * FROM amazon WHERE amazon.isbn = %s;', (isbn,)
        )
        amazon_reviews_dictionary = cursor.fetchall()
        amazon_reviews = [];
        for amazon_review_dictionary in amazon_reviews_dictionary:
            amazon_review = Amazon_review(amazon_review_dictionary)
            amazon_reviews.append(amazon_review)
        return amazon_reviews