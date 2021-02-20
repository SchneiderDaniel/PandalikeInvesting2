from flask import Flask, url_for
from flask_security import SQLAlchemySessionUserDatastore
from .extensions import mail, admin, security
from flask_admin.menu import  MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from importlib import import_module
from .models import User, Role, RolesUsers
from Dashapps import Dash_App1, Dash_App2
from os import path
import logging
from sqlalchemy.orm import scoped_session, sessionmaker
from .database import db_session, init_db


def register_extensions(app):
    # db.init_app(app)
    mail.init_app(app)
    
    
    
    # db.Model = automap_base(db.Model)
    # db_session = scoped_session(sessionmaker(autocommit=False,
    #                                      autoflush=False,
    #                                      bind=db))
    # user_datastore = SQLAlchemySessionUserDatastore(db_session,User, Role)
    # security.init_app(app,user_datastore)
    # Base.query = db_session.query_property()
    

def setup_security(app):
    # db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=db))
    user_datastore = SQLAlchemySessionUserDatastore(db_session,User, Role)
    security.init_app(app,user_datastore)
    # Base.query = db_session.query_property()

    return user_datastore

class MyAdminView(ModelView):

    def is_accessible(self):
        # is_admin = current_user.is_authenticated and current_user.username == app.config['ADMIN_USERNAME']
        # return is_admin
        return True

def init_admin(app):
    admin.init_app(app)
    admin.add_link(MenuLink(name='Go Back', category='', url='../'))
    admin.add_view(MyAdminView(User, db_session))
    admin.add_view(MyAdminView(Role, db_session))
    admin.add_view(MyAdminView(RolesUsers, db_session))

def register_blueprints(app):
    for module_name in ('base', 'home', 'tools', 'contact'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app, user_datastore):

    @app.before_first_request
    def initialize_database():
        # db.drop_all()
        # db.create_all()
        init_db()

        user_count = db_session.query(User).count()
        if user_count==0:
            print("Initialize Database")

            # defaultRole = Role(id=0, name='default')
            # defaultRole.add_to_db()

            # memberRole = Role(id=1,name='member')
            # memberRole.add_to_db()

            # adminRole = Role(id=2,name='admin')
            # adminRole.add_to_db()

            # User(id = 0, username=app.config['ADMIN_USERNAME'], email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASSWORD']).add_to_db()
            # RolesUsers(id=0,user_id=0,role_id=adminRole.id).add_to_db()

            user_datastore.create_role(name='default')
            user_datastore.create_role(name='member')
            user_datastore.create_role(name='admin')
            db_session.commit()

            user_datastore.create_user(email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASSWORD'], roles=['admin'])
            # user_datastore.create_user(email='matt@nobien.net', password='password',active=True)
            db_session.commit()

def configure_logs(app):
    # for combine gunicorn logging and flask built-in logging module
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    # endif



def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    user_datastore = setup_security(app)
    configure_database(app,user_datastore)
    init_admin(app)
    configure_logs(app)
    app = Dash_App1.Add_Dash(app)
    app = Dash_App2.Add_Dash(app)
    return app
