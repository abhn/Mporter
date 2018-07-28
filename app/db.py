from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_admin import Admin
from flask_security import current_user

_db = SQLAlchemy()


# Customized Role model for SQL-Admin
class SecureAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


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

    from .models import User, Role

    # add the admin panel views
    admin.add_view(SecureAdmin(Tasks, db.session))
    admin.add_view(SecureAdmin(Mentors, db.session))
    admin.add_view(SecureAdmin(Mentees, db.session))
    admin.add_view(SecureAdmin(User, db.session))
    admin.add_view(SecureAdmin(Role, db.session))

    # create all the models
    db.create_all()
    db.session.commit()

    return db
