from flask import Flask, render_template, request
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from .celery_utils import make_celery
import os
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY

admin = Admin(app, name='Mporter', template_mode='bootstrap3')

# the values of those depend on your setup

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

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

# -- celery stuff
app.config.update(
    CELERY_BROKER_URL=CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=CELERY_BROKER_URL
)
celery = make_celery(app)


from .utils import send_email_driver


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Sets up a celery scheduled task
    Can be used to call a routine at a particular interval or at some specific time of the day
    """
    # sender.add_periodic_task(
    #     crontab(hour=SEND_MAIL_HOUR),
    #     handle_mail.s(),
    # )
    sender.add_periodic_task(10.0, send_email_driver().s(), name='add every 10')


@celery.task
def handle_mail():
    """
    Just a helper method wrapped by celery.task.
    This will get called at the schedule descriped in @setup_periodic_tasks
    """
    send_email_driver()


# dummy route, TODO add a landing page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
