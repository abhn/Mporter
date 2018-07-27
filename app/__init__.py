from os import environ
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY
from .factory import create_app
from .db import db_config
from flask_security import Security, SQLAlchemyUserDatastore

app = create_app()
db_init = db_config(app)

# import celery stuff
from .celery_utils import *

# Setup Flask-Security
from .models import User, Role

user_datastore = SQLAlchemyUserDatastore(db_init, User, Role)
_security = Security(app, user_datastore)

from .views import before_first_request, index, mentee, new_task


if __name__ == '__main__':
    port = int(environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)
