from flask import Flask, render_template, request
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from os import environ
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY
from .factory import create_app

app = create_app()

admin = Admin(app, name='Mporter', template_mode='bootstrap3')

# initialize the db object
db = SQLAlchemy(app)
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

# import celery stuff
from .celery_utils import *

# dummy route, TODO add a landing page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
