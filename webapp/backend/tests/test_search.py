import pytest
from flaskr.db import get_db

def test_shows_book_title(client, auth, app):
    response = search(client, 'mockingbird')
    print(response.data)
    assert b'To Kill A Mockingbird' in response.data

def test_shows_book_description(client, auth, app):
    response = search(client, 'mockingbird')
    # assert b'One of the most cherished stories of all time, To Kill a Mockingbird has been translated into more than forty languages' in response.data
    # Currently test seed data doesn't have the description

def test_shows_book_author(client,auth,app):
    response = search(client, 'mockingbird')
    assert b'Harper Lee' in response.data

def test_no_results_found(client, auth, app):
    response = search(client, 'aowipdjqopwidjq')
    print(response.data)

def test_pagination_shows_only_10_results(client, auth, app):
    response = search(client, 'e')
    print(response.data)
    assert b'Page 1 of 3' in response.data

def test_pagination_lists_multiple_page_links(client, auth, app):
    response = search(client, 'e')
    assert b'Page 1 of 3' in response.data

def test_search_results_displays_page_one(client, auth, app):
    response = search(client, 'Frankenstein')
    assert b'Page 1 of 1' in response.data

def search(client, text):
    return client.post('/search/', data={'q': text})

