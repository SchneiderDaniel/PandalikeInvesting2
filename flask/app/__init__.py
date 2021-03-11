from flask import Flask, url_for, request
from flask_security import SQLAlchemySessionUserDatastore, current_user
from .extensions import mail, admin, security
from flask_admin.menu import  MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from importlib import import_module
from .models import User, Role, RolesUsers
from Dashapps import Dash_App1, Dash_App2, Dash_App3
from os import path
import logging
from sqlalchemy.orm import scoped_session, sessionmaker
from .database import db_session, init_db
from flask_security import LoginForm, url_for_security
from flask_security.utils import  encrypt_password
from datetime import datetime


def register_extensions(app):
    mail.init_app(app)

def setup_security(app):
    user_datastore = SQLAlchemySessionUserDatastore(db_session,User, Role)
    security.init_app(app,user_datastore)
    return user_datastore

class MyAdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

def init_admin(app):
    admin.init_app(app)
    admin.add_link(MenuLink(name='Go Back', category='', url='../'))
    admin.add_view(MyAdminView(User, db_session))
    admin.add_view(MyAdminView(Role, db_session))

def register_blueprints(app):
    for module_name in ('base', 'home', 'tools', 'contact'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app, user_datastore):

    @app.before_first_request
    def initialize_database():
        init_db()

        user_count = db_session.query(User).count()
        if user_count==0:
            print("Initialize Database")

            user_datastore.create_role(name='default')
            user_datastore.create_role(name='member')
            user_datastore.create_role(name='admin')
            db_session.commit()

            user_datastore.create_user(email='test@testdefault.de', username='testdefault', password= encrypt_password(app.config['ADMIN_PASSWORD']), roles=['default'], confirmed_at=datetime.now(), active=True)
            user_datastore.create_user(email='test@testmember.de', username='testmember', password= encrypt_password(app.config['ADMIN_PASSWORD']), roles=['member'], confirmed_at=datetime.now(), active=True)
            user_datastore.create_user(email=app.config['ADMIN_EMAIL'],username=app.config['ADMIN_USERNAME'], password= encrypt_password(app.config['ADMIN_PASSWORD']), roles=['admin'], confirmed_at=datetime.now(), active=True)
            db_session.commit()

def configure_logs(app):
    # for combine gunicorn logging and flask built-in logging module
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

def app_context(app):

    @app.context_processor
    def login_context():
        return {
            'url_for_security': url_for_security,
            # 'login_user_form': LoginForm(),
        }

    @app.context_processor
    def inject_template_scope():
        injections = dict()

        def cookies_check():
            value = request.cookies.get('my_cookie_consent')
            return value == 'true'
        injections.update(cookies_check=cookies_check)

        return injections

    @app.context_processor
    def year():
        current_year = datetime.now().year
        return dict(current_year = current_year) 
    


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    user_datastore = setup_security(app)
    configure_database(app,user_datastore)
    init_admin(app)
    configure_logs(app)
    app_context(app)
    app = Dash_App1.Add_Dash(app)
    app = Dash_App2.Add_Dash(app)
    app = Dash_App3.Add_Dash(app)
    return app
