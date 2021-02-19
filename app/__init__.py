from flask import Flask, url_for
from flask_login import current_user
from flask_security import SQLAlchemySessionUserDatastore
from .extensions import db, login_manager, mail, admin, security
from flask_admin.menu import  MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from importlib import import_module
from .base.models import User, Role, RolesUsers
from Dashapps import Dash_App1, Dash_App2
from os import path
import logging
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    init_admin()
    user_datastore = SQLAlchemySessionUserDatastore(db,User, Role)
    security.init_app(app,user_datastore)
    db.Model = automap_base(db.Model)

class MyView(ModelView):

    def is_accessible(self):
        # is_admin = current_user.is_authenticated and current_user.username == app.config['ADMIN']['username']
        # return is_admin
        return True

def init_admin():
    admin.add_link(MenuLink(name='Go Back', category='', url='../'))
    admin.add_view(MyView(User, db.session))
    admin.add_view(MyView(Role, db.session))
    admin.add_view(MyView(RolesUsers, db.session))

def register_blueprints(app):
    for module_name in ('base', 'home', 'tools', 'setting', 'contact'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()


        defaultRole = Role.query.filter_by(name='default').first()
        if defaultRole: defaultRole.delete_from_db()
        defaultRole = Role(id=0, name='default')
        defaultRole.add_to_db()

        memberRole = Role.query.filter_by(name='member').first()
        if memberRole: memberRole.delete_from_db()
        memberRole = Role(id=1,name='member')
        memberRole.add_to_db()

        adminRole = Role.query.filter_by(name='admin').first()
        if adminRole: adminRole.delete_from_db()
        adminRole = Role(id=2,name='admin')
        adminRole.add_to_db()
        

        admin_username = app.config['ADMIN']['username']
        user = User.query.filter_by(username=admin_username).first()
        if user: user.delete_from_db()
        admin_user = User(id = 0, **app.config['ADMIN'])
        admin_user.add_to_db()
        
        assign = RolesUsers.query.filter_by(user_id=0,role_id=2).first()
        if assign: assign.delete_from_db()
        RolesUsers(id=0,user_id=admin_user.id,role_id=adminRole.id).add_to_db()



    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def configure_logs(app):
    # for combine gunicorn logging and flask built-in logging module
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    # endif

# def apply_themes(app):

#     @app.context_processor
#     def override_url_for():
#         is_admin = current_user.is_authenticated and current_user.username == app.config['ADMIN']['username']
#         return dict(url_for = _generate_url_for_theme,
#                     Is_admin = is_admin )

#     def _generate_url_for_theme(endpoint, **values):
#         if endpoint.endswith('static'):
#             themename = values.get('theme', None) or \
#                 app.config.get('DEFAULT_THEME', None)
#             if themename:
#                 theme_file = "{}/{}".format(themename, values.get('filename', ''))
#                 if path.isfile(path.join(app.static_folder, theme_file)):
#                     values['filename'] = theme_file
#         return url_for(endpoint, **values)


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)
    # apply_themes(app)
    app = Dash_App1.Add_Dash(app)
    app = Dash_App2.Add_Dash(app)
    return app
