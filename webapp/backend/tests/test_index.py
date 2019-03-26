import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/');
    assert b"Welcome to BookBrain!" in response.data
    assert b"Your one stop shop for high quality aggregated reviews" in response.data
