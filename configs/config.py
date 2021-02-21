import os

class Config(object):
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    ADMIN_USERNAME = os.environ.get('ADMIN_USER')
    ADMIN_EMAIL = os.environ.get('ADMIN_MAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    SECURITY_PASSWORD_SALT = os.environ.get('SECRET_KEY')
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_URL_PREFIX = '/security'

class ProductionConfig(Config):
    DEBUG = False

class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
