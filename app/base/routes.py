from flask import jsonify, render_template, redirect, request, url_for
from . import blueprint


@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/about')
def about():
    return render_template('site_info/about.html')

@blueprint.route('/legal')
def legal():
    return render_template('site_info/legal.html')

@blueprint.route('/privacy')
def privacy():
    return render_template('site_info/privacy.html')

@blueprint.route('/terms')
def terms():
    return render_template('site_info/terms.html')


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
