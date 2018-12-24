# run.py

import os

from netops import create_app
from netops.utils.database import first_start

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


if __name__ == '__main__':
    with app.app_context():
        first_start()

    app.run()
