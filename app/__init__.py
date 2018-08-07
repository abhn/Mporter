from os import environ
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY
from .factory import create_app
from .db import db_config
from flask_security import Security, SQLAlchemyUserDatastore
from .api import api_init


app = create_app()
db_init = db_config(app)
api_init(app)

user_datastore = None


def misc_init(app, db_init):
    # Setup Flask-Security
    from .models import User, Role

    global user_datastore
    user_datastore = SQLAlchemyUserDatastore(db_init, User, Role)
    _security = Security(app, user_datastore)

    from .views import before_first_request, index, mentee, new_task

    return user_datastore


misc_init(app, db_init)

# import celery stuff
from .celery_utils import *

if __name__ == '__main__':
    port = int(environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)
