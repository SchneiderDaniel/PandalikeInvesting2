import os

class Config(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = {'username': os.environ.get('ADMIN_USER'),
             'email': os.environ.get('ADMIN_EMAIL'),
             'password':  os.environ.get('ADMIN_PASSWORD')}

    # THEME SUPPORT
    #  if set then url_for('static', filename='', theme='')
    #  will add the theme name to the static URL:
    #    /static/<DEFAULT_THEME>/filename
    # DEFAULT_THEME = "themes/dark"
    DEFAULT_THEME = None


class ProductionConfig(Config):
    DEBUG = False

  




    # PostgreSQL database
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    #     os.environ.get('DATABASE_USER'),
    #     os.environ.get('DATABASE_PASSWORD'),
    #     os.environ.get('DATABASE_HOST'),
    #     os.environ.get('DATABASE_PORT'),
    #     os.environ.get('DATABASE_NAME')
    # )

    


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
