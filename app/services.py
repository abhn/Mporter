from app import user_datastore, db_init
from datetime import datetime, timedelta


def get_mentee_tasks(user_id):
    """helper function to get user's tasks"""

    from .models import Tasks

    user_tasks = Tasks\
        .query\
        .filter_by(mentee_id=user_id) \
        .filter(Tasks.at_created >= datetime.today() - timedelta(days=1))\
        .all()

    return user_tasks


def get_mentee_mentors(user_id):
    """helper function to get user's mentors"""

    from .models import Mentees
    mentee_mentors = Mentees.query.filter_by(id=user_id).first()
    return mentee_mentors.mentor


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

    task = Tasks(mentee_id=current_user_id, task=task)

    db_init.session.add(task)
    db_init.session.commit()


def add_mentor(mentor_name, mentor_email, current_user_id):
    from .models import Mentors, Mentees

    # something's fishy, return
    if not mentor_name or not mentor_email:
        return

    mentee_present = Mentees.query.filter_by(id=current_user_id).first()

    if not mentee_present:
        return

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

    db_init.session.commit()


