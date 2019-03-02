from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('about', __name__)

@bp.route('/about', methods=['GET'])
def show():
    return render_template('about/about.html')
