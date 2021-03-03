from flask_migrate import Migrate
from configs.config import config_dict
from app import create_app
import os
import sys

get_config_mode = os.environ.get('CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    sys.exit('Error: Invalid CONFIG_MODE environment variable entry.')

app = create_app(config_mode)
# Migrate(app, db)

if __name__ == "__main__":
    app.run(port=5001, debug = True, threaded=False)