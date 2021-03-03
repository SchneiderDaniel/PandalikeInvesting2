from app import create_app
import sys
import os
from configs.config import config_dict
from app.database import drop_db

get_config_mode = os.environ.get('CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    sys.exit('Error: Invalid CONFIG_MODE environment variable entry.')

app = create_app(config_mode)

app.app_context().push()

print('This is the DB Path', file=sys.stderr)
print(app.config['SQLALCHEMY_DATABASE_URI'])
print('Dropping Database...', file=sys.stderr)
drop_db()

print('Database dropped!', file=sys.stderr)



 