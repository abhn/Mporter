from testing.postgresql import Postgresql

import pytest

from app.factory import create_app
from app.db import db_config

from flask_sqlalchemy import SQLAlchemy

from app.app_config import DB_URL_TEST

_db = SQLAlchemy()


from app.models import Tasks


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'test'
    TESTING = True
    SQLALCHEMY_DATABASE_URI=DB_URL_TEST


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app(TestConfig)
    db_config(_app)
    with Postgresql() as postgresql:
        _app.config['SQLALCHEMY_DATABASE_URI'] = postgresql.url()
        ctx = _app.app_context()
        ctx.push()

        yield _app

        ctx.pop()


@pytest.fixture(scope='session')
def testapp(app):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


def test_admin_landing(testapp):
    """test if landing page works"""

    rv = testapp.get('/admin/')
    assert rv.status == '200 OK'

