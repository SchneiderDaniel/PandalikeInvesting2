from . import blueprint
from flask import render_template
from Dashapps import Dash_App1, Dash_App2, Dash_App3
from flask_security import login_required, roles_accepted


@blueprint.route('/rebalancing')
# @login_required
def app1_template():
    return render_template('app1.html', dash_url = Dash_App1.url_base)

@blueprint.route('/correlation')
# @login_required
# @roles_accepted('admin')
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base)


@blueprint.route('/impactoffondcosts')
def app3_template():
    return render_template('app3.html', dash_url = Dash_App3.url_base)