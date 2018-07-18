from celery import Celery
from app import app
from .app_config import SEND_MAIL_HOUR, CELERY_BROKER_URL, DB_URL, SECRET_KEY


def make_celery(app):
    """
    A textbook celery creation util that creates a celery instance with the proper config and returns the instance
    :param app: flask app instance
    :return: celery instance
    """
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


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
