import pytest
from flaskr.db import get_db

def test_shows_about_message(client, auth, app):
    html = client.get("/about").data
    assert b'About BookBrain'
    assert b'The goal of BookBrain is simple: B' in html
    assert b' sources aggregated in one place.' in html

def test_shows_team_bios(client, auth, app):
    html = client.get("/about").data
    assert b'The BookBrain Team' in html

def test_shows_sources_tools_github(client, auth, app):
    html = client.get("/about").data
    assert b'Sources, Tools, and Github' in html

def test_shows_stats(client, auth, app):
    html = client.get("/about").data
    assert b'Stats' in html
    assert b'Total Unit Tests:' in html
    assert b'Total Github Issues:' in html
    assert b'Total Commits:' in html
