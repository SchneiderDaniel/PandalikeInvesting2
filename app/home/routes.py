from . import blueprint
from flask import render_template
from flask_login import login_required, current_user


@blueprint.route('/')
def index():
    return render_template('index.html')