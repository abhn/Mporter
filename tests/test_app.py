from flask import Flask
import pytest
from app.factory import create_app
from flask_sqlalchemy import SQLAlchemy
from app.app_config import DB_URL_TEST
from app.db import db_config, _db
from app.celery_utils import make_celery
from celery import Celery
from utils import  get_env_var
from app.utils import send_mail, send_email_driver
import json

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
    """test db create"""

    mentor = Mentors(mentor_name='test123mentor', mentor_email='test1234@test1234.com')
    mentee = Mentees(mentee_name='test123mentee')

    mentor.mentee.append(mentee)

    session.add_all([mentor])
    session.commit()

    task = Tasks(task='this is a test task', mentee_id=mentee.id)

    session.add(task)
    session.commit()

    assert mentor and mentee and task in session


def test_db_modal_read(session):
    """test db reads"""

    mentor = Mentors(mentor_name='test123mentor', mentor_email='test1234@test1234.com')

    mentee1 = Mentees(mentee_name='test123mentee')
    mentee2 = Mentees(mentee_name='test456mentee')

    mentor.mentee.append(mentee1)
    mentor.mentee.append(mentee2)

    session.add_all([mentor])
    session.commit()

    task1 = Tasks(task='task 1', mentee_id=mentee1.id)
    task2 = Tasks(task='task 2', mentee_id=mentee2.id)

    session.add_all([task1, task2])

    session.commit()

    mentors_var = Mentors.query.all()
    # one row in mentors table
    assert len(mentors_var) == 1

    mentees_var = Mentees.query.all()
    # two row in mentees table
    assert (len(mentees_var)) == 2

    mentor_to_check = mentors_var[0]
    assert mentor_to_check.mentor_name == 'test123mentor' and mentor_to_check.id > 0

    assert len(mentor_to_check.mentee) == 2

    assert mentor_to_check.mentee[0].mentee_name == 'test123mentee' \
        and mentor_to_check.mentee[1].mentee_name == 'test456mentee'

    tasks_var = Tasks.query.all()
    assert len(tasks_var) == 2

    for task in tasks_var:
        assert task.mentee_id > 0


def test_factory_create_app():
    """test if app factory returns an instance of Flask"""

    app_instance = create_app()

    assert isinstance(app_instance, Flask)


def test_factory_make_celery():
    """test if celery factory returns an instance of Celery"""

    app_instance = create_app()
    celery_instance = make_celery(app_instance)

    assert isinstance(celery_instance, Celery)


def test_env_vars():
    """test if the critical env variables are available in the environment"""

    CELERY_BROKER_URL = get_env_var('CELERY_BROKER_URL')

    DB_URL = get_env_var('SQLALCHEMY_DATABASE_URI')
    DB_URL_TEST = get_env_var('SQLALCHEMY_DATABASE_URI_TEST')

    SECRET_KEY = get_env_var('MPORTER_SECRET')

    MAILGUN_KEY = get_env_var('MAILGUN_KEY')
    MAILGUN_SANDBOX = get_env_var('MAILGUN_SANDBOX')

    assert CELERY_BROKER_URL is not None
    assert DB_URL is not None
    assert DB_URL_TEST is not None
    assert SECRET_KEY is not None
    assert MAILGUN_KEY is not None
    assert MAILGUN_SANDBOX is not None


def test_send_mail():
    """should fail on incorrect email address"""

    rv = send_mail('', 'hello, this is testing!')

    rv_obj = json.loads(rv)

    assert rv_obj['message'] == "'to' parameter is not a valid address. please check documentation"

    # change email
    rv = send_mail('testingmportertesting@gmail.com', 'hello, this is testing!')
    rv_obj = json.loads(rv)

    assert 'id' in rv_obj


def test_send_mail_driver(session):
    """to test this function, it is sufficient to verify that right number of emails are staged for sending"""

    mentor1 = Mentors(mentor_name='test1mentor', mentor_email='test1@test1.com')
    mentor2 = Mentors(mentor_name='test2mentor', mentor_email='test2@test2.com')
    mentor3 = Mentors(mentor_name='test3mentor', mentor_email='test3@test3.com')

    mentee1 = Mentees(mentee_name='test123mentee')
    mentee2 = Mentees(mentee_name='test456mentee')

    mentor1.mentee.append(mentee1)
    mentor2.mentee.append(mentee2)

    mentor3.mentee.append(mentee1)
    mentor3.mentee.append(mentee2)

    session.add_all([mentor1, mentor2, mentor3])
    session.commit()

    task1 = Tasks(task='task 1', mentee_id=mentee1.id)
    task2 = Tasks(task='task 2', mentee_id=mentee2.id)
    task3 = Tasks(task='task 3', mentee_id=mentee2.id)

    session.add_all([task1, task2, task3])
    session.commit()

    email_count = send_email_driver(is_test=True)  # set is_test=True to not send an actual email

    # mentor1 - 1
    # mentor2 - 1
    # mentor3 - 2
    # total emails to send - 4
    assert email_count == 4
