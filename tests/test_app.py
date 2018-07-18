from testing.postgresql import Postgresql
import pytest
from app.factory import create_app
from flask_sqlalchemy import SQLAlchemy
from app.app_config import DB_URL_TEST
from app.db import db_config, _db


from app.models import Tasks, Mentees, Mentors


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'test'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DB_URL_TEST


@pytest.fixture(scope='session')
def app():
    _app = create_app(TestConfig)
    db_config(_app)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def testapp(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


def test_admin_landing(testapp):
    """test if landing page works"""

    rv = testapp.get('/admin/')
    assert rv.status == '200 OK'


def test_db_instance_of_sqlalchemy(db):
    """test if db is not None, and is an instance of SQLalchemy class"""
    assert isinstance(db, SQLAlchemy)


def test_db_modal_create(session):
    # task = Tasks(task='this is a test task', mentee_id=1)
    mentor = Mentors(mentor_name='test123mentor', mentor_email='test1234@test1234.com')
    mentee = Mentees(mentee_name='test123mentee')

    # session.add(task)
    session.add(mentor)
    session.add(mentee)

    session.commit()

    # assert task in session
    assert mentor in session
    assert mentee in session


def test_db_modal_read(db):
    pass