from app import user_datastore, db_init
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import InvalidUsage


def get_mentee_tasks(user_id):
    """helper function to get user's tasks"""

    from .models import Tasks

    user_tasks = Tasks\
        .query\
        .filter_by(mentee_id=user_id) \
        .filter(Tasks.at_created >= datetime.today() - timedelta(days=1))\
        .all()

    return user_tasks


def get_mentee_tasks_dict(user_id):
    """return tasks as a list of dicts"""

    tasks = get_mentee_tasks(user_id)

    obj = []
    for task in tasks:
        obj.append({'id': task.id, 'task': task.task, 'at_created': str(task.at_created)})

    return obj


def get_mentee_mentors(user_id):
    """helper function to get user's mentors"""

    from .models import Mentees
    mentee_mentors = Mentees.query.filter_by(id=user_id).first()
    return mentee_mentors.mentor


def get_mentee_mentors_dict(user_id):
    """return mentors as a list of dicts"""

    mentors = get_mentee_mentors(user_id)

    obj = []
    for mentor in mentors:
        obj.append({'id': mentor.id, 'mentor_name': mentor.mentor_name, 'mentor_email': mentor.mentor_email})

    return obj


def get_mentee_data(current_user_id):
    """curate data used by /mentee view"""

    from .models import Mentees

    user = user_datastore.get_user(current_user_id)

    # in case no user currently logged in, fetch user from mentee model
    if user is None:
        user = Mentees.query.filter_by(id=current_user_id).first()
        user_email = user.mentee_email
    else:
        user_email = user.email

    try:
        is_admin = True if user.roles[0].name == 'admin' else False
    except AttributeError:
        is_admin = False
    except IndexError:
        is_admin = False

    user_tasks = get_mentee_tasks(current_user_id)

    user_obj = {
        'user_id': user.id,
        'user_email': user_email,
        'user_tasks': user_tasks,
        'user_mentors': get_mentee_mentors(current_user_id),
        'is_admin': is_admin
    }

    return user_obj


def add_task(current_user_id, task):
    """get user_id and task and add that task for that user. Assume authentication"""

    from .models import Tasks

    try:
        task = Tasks(mentee_id=current_user_id, task=task)
        db_init.session.add(task)
        db_init.session.commit()
        return True

    except SQLAlchemyError:
        raise InvalidUsage(status_code=400)


def add_mentor(mentor_name, mentor_email, current_user_id):
    """
    create a new mentor and add mentee current user. If user already present, just add mentee.
    :param mentor_name:
    :param mentor_email:
    :param current_user_id:
    :return: None
    """

    from .models import Mentors, Mentees

    # something's fishy, return
    if not mentor_name or not mentor_email:
        return False

    mentee_present = Mentees.query.filter_by(id=current_user_id).first()

    if not mentee_present:
        raise InvalidUsage(status_code=400)

    # check if the mentor is present
    mentor_present = Mentors.query.filter_by(mentor_email=mentor_email).first()

    if not mentor_present:
        # create the mentor
        new_mentor_create = Mentors(mentor_name=mentor_name, mentor_email=mentor_email)
        new_mentor_create.mentee.append(mentee_present)
        db_init.session.add(new_mentor_create)
    else:
        # just add our mentee to that mentor
        mentor_present.mentee.append(mentee_present)
        db_init.session.add(mentor_present)

    try:
        db_init.session.commit()
        return True

    except SQLAlchemyError:
        raise InvalidUsage(status_code=500)


def delete_task(current_user_id, task_id):
    from .models import Tasks, Mentees

    mentee = Mentees.query.filter_by(id=current_user_id).first()

    task = Tasks.query.filter_by(id=task_id).first()

    # bad mentee or task id supplied
    if not mentee or not task:
        raise InvalidUsage(status_code=400)

    # unauthorized
    if task.mentee_id is not mentee.id:
        raise InvalidUsage(status_code=403)
    
    try:
        db_init.session.delete(task)
        db_init.session.commit()
    except SQLAlchemyError:
        raise InvalidUsage(status_code=500)    


def delete_mentor(current_user_id, mentor_id):
    from .models import Mentees, Mentors

    mentee = Mentees.query.filter_by(id=current_user_id).first()
    mentor = Mentors.query.filter_by(id=mentor_id).first()

    # bad mentee or mentor id supplied
    if not mentee or not mentor:
        raise InvalidUsage(status_code=400)

    try:
        mentee.mentor.remove(mentor)
        db_init.session.add(mentee)
        db_init.session.commit()
    except SQLAlchemyError:
        raise InvalidUsage(status_code=500)
    