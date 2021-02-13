from . import blueprint
from flask import render_template
from flask_login import login_required
from Dashapps import Dash_App1, Dash_App2

@blueprint.route('/app1')
def app1_template():
    return render_template('app1.html', dash_url = Dash_App1.url_base)

@blueprint.route('/app2')
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base)