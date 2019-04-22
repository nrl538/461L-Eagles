from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory('/static/favicon.ico', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

