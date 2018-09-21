from flask_security import login_required, current_user
from flask import render_template, request, url_for, redirect
from app import user_datastore, app, db_init
from flask_security.utils import hash_password
from .services import get_mentee_data, add_task, add_mentor
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import InvalidUsage


@app.before_first_request
def before_first_request():
    """
    runs before the first request, adds an user account and sets it as 'admin' role.
    """

    # create admin and normal user roles
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='End user')

    # create an admin user and add to database
    encrypted_password = hash_password('password')
    if not user_datastore.get_user('admin@mporter.co'):
        user_datastore.create_user(email='admin@mporter.co', password=encrypted_password)

    try:
        db_init.session.commit()
    except SQLAlchemyError:
        raise InvalidUsage(status_code=500)

    # make admin@mporter.co the admin user
    user_datastore.add_role_to_user('admin@mporter.co', 'admin')
    try:
        db_init.session.commit()
    except SQLAlchemyError:
        raise InvalidUsage(status_code=500)


@app.route('/')
def index():
    """
    serves the static index page with features and stuff
    """
    return render_template('index.html')


@app.route('/mentee')
@login_required
def mentee():
    """
    serves a page with tasks by the mentee and a form to add new tasks
    additionally a button to logout. Admin gets a button to access admin panel. KISS.
    """
    current_user_id = current_user.get_id()
    user_obj = get_mentee_data(current_user_id)
    return render_template('mentee.html', user=user_obj)


@app.route('/new-task', methods=['POST'])
@login_required
def new_task():
    """
    An api to add a new task. API needs authentication, and the task will be added to the authenticated user's tasks.
    @:param task: text of the task to be added in post request body
    """
    task = request.form.get('task')
    current_user_id = current_user.get_id()

    add_task(current_user_id, task)

    return redirect(url_for('mentee'))


@app.route('/new-mentor', methods=['POST'])
@login_required
def new_mentor():
    """
    add a mentor to user's mentors list. If mentor is not present, add a new mentor as well with the name supplied
    note that if a mentor is present, the mentor_name supplied by user is ignored
    @:param: mentor-name, mentor-email
    """
    # from .models import Mentors, Mentees

    mentor_name = request.form.get('mentor-name')
    mentor_email = request.form.get('mentor-email')
    current_user_id = current_user.get_id()

    add_mentor(mentor_name, mentor_email, current_user_id)

    return redirect(url_for('mentee'))


@app.route('/beta')
def beta():
    return render_template('pwa.html')