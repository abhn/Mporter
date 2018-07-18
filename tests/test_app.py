import os
import tempfile

import pytest

from app import app
from flask_sqlalchemy import SQLAlchemy

from app import db
from app.models import Tasks, Mentees, Mentors
import unittest
from flask_testing import TestCase
import os


@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI_TEST']
    app.config['TESTING'] = True

    client = app.test_client()

    # with app.app_context():
    #     app.init_db()

    yield client


def test_landing_page(client):
    """testing if test suite works"""

    rv = client.get('/')
    assert b'hello world' in rv.data


def test_models(client):

    db = SQLAlchemy(client)

    # create all the models
    db.create_all()
    db.session.commit()

    # create a mentee
    mentee = Mentees(mentee_name='test_mentee_123')

    db.session.add(mentee)
    db.session.commit()

    assert mentee in db.session
