from flask_restful import Resource, reqparse
from flask_security import current_user, auth_token_required
from flask_security.utils import verify_password
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Api


class MporterAPIAuth(Resource):
    def post(self):
        """Logs a user in
        @:param: email, password in form data
        @:return: {token: token} authorization token
        """

        from .models import User

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Email of user')
        parser.add_argument('password', type=str, help='Password of user')
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()

        try:
            if verify_password(password=args['password'], password_hash=user.password):
                # we can even send remember me cookies and session id, but let's not do it for rest
                # login_user(user, remember=True)
                is_admin = len([role for role in user.roles if role.name == 'admin']) == 1
                return {'token': user.get_auth_token(), 'success': True, 'is_admin': is_admin}, 200
            else:
                return {'token': None, 'success': False}, 401
        except AttributeError:
            return {'token': None, 'success': False}, 401


class MporterAPITask(Resource):
    @auth_token_required
    def get(self):
        """
        get user tasks
        jwt authorization header required
        :return: {tasks: [list of tasks]}
        """

        from .services import get_mentee_tasks_dict

        user_id = current_user.get_id()
        try:
            tasks = get_mentee_tasks_dict(user_id)
            return {'tasks': tasks, 'success': True}, 200
        except SQLAlchemyError:
            return {'success': False}

    @auth_token_required
    def post(self):
        """
        create new task under the authorized user
        :return: {message: 'success' or 'failed'}
        """

        from .services import add_task
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str, help='Task of user')
        args = parser.parse_args()

        try:
            add_task(current_user.get_id(), args['task'])
            return {'success': True}, 201
        except SQLAlchemyError:
            return {'success': False}, 500

    @auth_token_required
    def delete(self):
        """
        delete a task under the authorized user
        """
        from .services import delete_task
        parser = reqparse.RequestParser()
        parser.add_argument('task_id', type=int, help='ID of the task')

        args = parser.parse_args()

        try:
            delete_task(current_user.get_id(), args['task_id'])
            return {'success': True}, 200
        except SQLAlchemyError:
            return {'success': False}, 500



class MporterAPIMentor(Resource):
    @auth_token_required
    def get(self):
        """
        get logged in mentee's mentors
        :return: {'mentors': [list of mentors]
        """
        from .services import get_mentee_mentors_dict

        user_id = current_user.get_id()

        try:
            mentors = get_mentee_mentors_dict(user_id)
            return {'mentors': mentors, 'success': True}
        except SQLAlchemyError:
            return {'success': False}

    @auth_token_required
    def post(self):
        """create or add mentor under the authorized user"""

        from .services import add_mentor

        parser = reqparse.RequestParser()
        parser.add_argument('mentor_name', type=str, help='Name of mentor')
        parser.add_argument('mentor_email', type=str, help='Email of mentor')
        args = parser.parse_args()

        try:
            add_mentor(args['mentor_name'], args['mentor_email'], current_user.get_id())
            return {'success': True}, 201
        except SQLAlchemyError:
            return {'success': False}, 500
    
    @auth_token_required
    def delete(self):
        """
        delete a mentor from under the logged in user
        """

        from .services import delete_mentor
        parser = reqparse.RequestParser()
        parser.add_argument('mentor_id', type=str, help='ID of mentor')
        args = parser.parse_args()

        try:
            delete_mentor(current_user.get_id(), args['mentor_id'])
            return {'success': True}, 200
        except SQLAlchemyError:
            return {'success': False}, 500


def api_init(app):
    api = Api(app)

    api.add_resource(MporterAPIAuth, '/api/auth')
    api.add_resource(MporterAPITask, '/api/task')
    api.add_resource(MporterAPIMentor, '/api/mentor')
