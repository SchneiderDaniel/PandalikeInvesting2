# from app import create_app
# import sys, os
# from configs.config import config_dict

# get_config_mode = os.environ.get('CONFIG_MODE', 'Debug')

# try:
#     config_mode = config_dict[get_config_mode.capitalize()]
# except KeyError:
#     sys.exit('Error: Invalid CONFIG_MODE environment variable entry.')

# app = create_app(config_mode)
# app.app_context().push()

# from app import db

# # db.create_all()

# print('This is the DB Pathc', file=sys.stderr)
# print(app.config['SQLALCHEMY_DATABASE_URI'])
# print('Dropping Database...', file=sys.stderr)
# db.drop_all()
# print('Database dropped!', file=sys.stderr)

# print('Reinitializing Database..', file=sys.stderr)
# db.create_all()
# print('Database reinitialized!', file=sys.stderr)

