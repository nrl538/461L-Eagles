import pytest
from flaskr.db import get_db

def test_shows_book_title(client, auth, app):
    response = client.post('/search/', data = {'q': 'mockingbird'} )
    assert b'To Kill A Mockingbird' in response.data

def test_shows_book_description(client, auth, app):
    response = client.post('/search/', data = {'q': 'mockingbird'} )
    assert b'The unforgettable novel of a childhood in a sleepy Southern' in response.data

def test_shows_book_author(client,auth,app):
    response = client.post('/search/', data = {'q': 'mockingbird'} )
    assert b'Harper Lee' in response.data

def test_shows_book_publish_date(client,auth,app):
    response = client.post('/search/', data = {'q': 'mockingbird'} )
    assert b'1988-10-11' in response.data

def test_no_results_found(client, auth, app):
    response = client.post('/search/', data = {'q': 'aowipdjqopwidjq'} )
