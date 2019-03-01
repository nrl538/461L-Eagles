from flask import current_app, g
from flask.cli import with_appcontext
import click
import MySQLdb
import MySQLdb.cursors

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect(host="127.0.0.1",  # your host 
                     user="bookbrain",       # username
                     passwd="461leagles",     # password
                     db="bookbrain",# name of the database
                     cursorclass=MySQLdb.cursors.DictCursor)   
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))

    if cursor:
        cursor.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
