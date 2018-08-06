from flask_restful import Resource, reqparse
from flask_security import login_required, current_user, auth_token_required
from flask_security.utils import login_user, hash_password, verify_password
from flask import Flask, request
from sqlalchemy.exc import SQLAlchemyError
import json


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
                return {'token': user.get_auth_token()}, 200
            else:
                return {'token': None}, 401
        except AttributeError:
            return {'token': None}, 401


class MporterAPITask(Resource):
    @auth_token_required
    def get(self):
        from .services import get_mentee_tasks_dict

        user_id = current_user.get_id()
        tasks = get_mentee_tasks_dict(user_id)

        return {'tasks': tasks}

    @auth_token_required
    def post(self):
        """create new task under the authorized user"""

        from .services import add_task
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str, help='Task of user')
        args = parser.parse_args()

        try:
            add_task(current_user.get_id(), args['task'])
            return {'message': 'success'}, 201
        except SQLAlchemyError:
            return {'message': 'failed'}, 500


class MporterAPIMentor(Resource):
    @auth_token_required
    def get(self):
        from .services import get_mentee_mentors_dict

        user_id = current_user.get_id()
        mentors = get_mentee_mentors_dict(user_id)

        return {'mentors': mentors}

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
            return {'message': 'success'}, 201
        except SQLAlchemyError:
            return {'message': 'failure'}, 500
