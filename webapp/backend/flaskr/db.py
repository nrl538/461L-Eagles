import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import MySQLdb
import MySQLdb.cursors

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        '''
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        '''
        #35.192.163.20
        g.db = MySQLdb.connect(host="35.192.163.20",  # your host 
                     user="root",       # username
                     passwd="root",     # password
                     db="mysqldb",# name of the database
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

    with current_app.open_resource('schema.sql') as f:
        text = f.read().decode('utf8')
    sql_commands = text.split(';')
    for i in range(len(sql_commands)):
        if (i==len(sql_commands)-1):
            break
        command = sql_commands[i].replace('\n','')
        command =command.replace('\t','')+';'
        db.cursor().excute(command)
    
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
