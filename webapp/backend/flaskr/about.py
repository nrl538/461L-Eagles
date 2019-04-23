from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import subprocess
import re

bp = Blueprint('about', __name__)

@bp.route('/about', methods=['GET'])
def show():
    commits = "\n" + get_commits().decode('ascii', 'ignore')
    return render_template('about/about.html', commits=commits)

# Not dealing with pulling all commits individually, so for now, just list the console
# output of `git shortlog -s -n`
# contributed_commits = re.findall(b'.*?(\d{1,3})\s(\w*?)\s', result)
def get_commits():
    result = subprocess.check_output(['git', 'shortlog', '-s', '-n'], stdout=subprocess.PIPE).stdout
    return result
