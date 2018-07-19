from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_admin import Admin

_db = SQLAlchemy()


def db_config(app):
    """
    initialize database related stuff
    :param app: flask app instance
    :return: None
    """
    admin = Admin(app, name='Mporter', template_mode='bootstrap3')

    # initialize the db object
    db = SQLAlchemy(app)
    global _db
    _db = db
    migrate = Migrate(app, db)

    # now import models to prevent cylic import errors,
    # there has to be a better way to do this, sigh.
    from .models import Tasks, Mentees, Mentors

    # add the admin panel views
    admin.add_view(ModelView(Tasks, db.session))
    admin.add_view(ModelView(Mentors, db.session))
    admin.add_view(ModelView(Mentees, db.session))

    # create all the models
    db.create_all()
    db.session.commit()

    return db
