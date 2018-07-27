from flask_security import login_required, current_user
from flask import render_template, request, url_for, redirect
from app import user_datastore, app, db_init
from flask_security.utils import hash_password


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

    db_init.session.commit()

    # make admin@mporter.co the admin user
    user_datastore.add_role_to_user('admin@mporter.co', 'admin')
    db_init.session.commit()


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
    additionally a button to logout. KISS.
    """
    current_user_id = current_user.get_id()
    user = user_datastore.get_user(current_user_id)

    from .models import Tasks

    user_tasks = Tasks.query.filter_by(mentee_id=user.id).all()

    user_obj = {
        'user_id': user.id,
        'user_email': user.email,
        'user_tasks': user_tasks
    }

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
    user = user_datastore.get_user(current_user_id)

    from .models import Tasks

    task = Tasks(mentee_id=user.id, task=task)

    db_init.session.add(task)
    db_init.session.commit()

    return redirect(url_for('mentee'))

