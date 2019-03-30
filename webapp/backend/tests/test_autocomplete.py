import pytest
from flaskr.db import get_db

def test_autocompletes_author_name_with_case(client, auth, app):
    response = client.get('/search/names', query_string={'term': 'To K', 'cat': 'Title'})
    assert b'To Kill A Mockingbird' in response.data

def test_autocompletes_author_name_case_insensitive(client, auth, app):
    response = client.get('/search/names', query_string={'term': 'to k', 'cat': 'Title'})
    assert b'To Kill A Mockingbird' in response.data

