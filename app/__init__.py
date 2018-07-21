from flask import render_template
from os import environ
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY
from .factory import create_app
from .db import db_config

app = create_app()
db_config(app)

# import celery stuff
from .celery_utils import *


# dummy route, TODO add a landing page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(environ.get('PORT', 33507)) #
    app.run(host='0.0.0.0', port=port)
