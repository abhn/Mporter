from flask import render_template
from os import environ
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY
from .factory import create_app
from .db import db_config
from flask_security import Security, SQLAlchemyUserDatastore, login_required, roles_required, utils, current_user, UserMixin

app = create_app()
db_init = db_config(app)

# import celery stuff
from .celery_utils import *

user_datastore = None


@app.before_first_request
def before_first_request():

    # Setup Flask-Security
    from .models import User, Role
    global user_datastore
    user_datastore = SQLAlchemyUserDatastore(db_init, User, Role)
    _security = Security(app, user_datastore)

    # # create admin and normal user roles
    # user_datastore.find_or_create_role(name='admin', description='Administrator')
    # user_datastore.find_or_create_role(name='user', description='End user')
    #
    # # create an admin user and add to database
    # encrypted_password = 'password'
    # if not user_datastore.get_user('admin4@test.com'):
    #     user_datastore.create_user(email='admin4@test.com', password=encrypted_password)
    #
    # db_init.session.commit()
    #
    # # make admin@test.com the admin user
    # user_datastore.add_role_to_user('admin4@test.com', 'admin')
    db_init.session.commit()


# dummy route, TODO add a landing page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentee')
@login_required
def mentee():
    current_user_id = current_user.get_id()
    user = user_datastore.get_user(current_user_id)

    user_obj = {
        'user_id': user.id,
        'user_email': user.email
    }

    return render_template('mentee.html', user=user_obj)


if __name__ == '__main__':
    port = int(environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)
