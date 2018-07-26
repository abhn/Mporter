from .app_config import DB_URL, SECRET_KEY, CELERY_BROKER_URL, \
    BASIC_AUTH_FORCE, BASIC_AUTH_PASSWORD, BASIC_AUTH_REALM, BASIC_AUTH_USERNAME
from flask_basicauth import BasicAuth
from flask import Flask


class DevConfig(object):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = CELERY_BROKER_URL
    BASIC_AUTH_USERNAME = BASIC_AUTH_USERNAME
    BASIC_AUTH_PASSWORD = BASIC_AUTH_PASSWORD
    BASIC_AUTH_FORCE = BASIC_AUTH_FORCE
    BASIC_AUTH_REALM = BASIC_AUTH_REALM
    SECURITY_PASSWORD_SALT = 'unique_salt_3315'
    SECURITY_REGISTERABLE = True
    TESTING = False

# _db = SQLAlchemy()


def create_app(config=None):
    """
    app factory function, creates a new Flask app instance and returns. Optionally creates an app using the config supplied
    :param config: custom config, used in testing
    :return: Flask app instance
    """

    app = Flask(__name__, instance_relative_config=True, static_folder='../static')

    # basic auth only in deployment
    # if not app.config['TESTING']:
    #     basic_auth = BasicAuth(app)

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(DevConfig)
    else:
        # load the test config if passed in
        app.config.from_object(config)

    return app
