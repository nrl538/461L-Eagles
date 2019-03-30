import pytest
from flaskr.db import get_db

def test_shows_book_title(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Frankenstein' in response.data

def test_shows_book_rating(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'BookBrain Averaged Internet Rating: 0.0' in response.data
    assert b'This rating is based on a weighted sum of ratings and reviews pulled from multiple other websites and sources.' in response.data

def test_shows_critic_review(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Critic Review' in response.data

def test_shows_audience_review(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Audience Review' in response.data

def test_shows_cover(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'alt="Frankenstein - Book Cover"' in response.data

def test_shows_author(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Mary Wollstonecraft Shelley' in response.data

def test_shows_description(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Description' in response.data

def test_shows_similar_books(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Similar books' in response.data

def test_shows_details(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Details' in response.data

def test_shows_purchase_link(client, auth, app):
    response = go_to_frankenstein(client, app)
    assert b'Links to purchase' in response.data

def test_shows_under_construction_text_with_invalid_book_id(client, auth, app):
    response = client.get("/book/20192302193")
    assert b'Sorry, but BookBrain is still undergoing development, and we do not currently have this book listed.' in response.data

def go_to_frankenstein(client, app):
    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute("select books.id from books where books.title = 'Frankenstein'",)
        book = cursor.fetchone()
        assert book is not None

    return client.get("/book/%s" % book['id'])
