from .app_config import DB_URL, SECRET_KEY

from flask import Flask


class DevConfig(object):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# _db = SQLAlchemy()


def create_app(config=None):
    """
    app factory function, creates a new Flask app instance and returns. Optionally creates an app using the config supplied
    :param config: custom config, used in testing
    :return: Flask app instance
    """

    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(DevConfig)
    else:
        # load the test config if passed in
        app.config.from_object(config)

    return app
