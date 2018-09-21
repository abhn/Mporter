from flask import jsonify
from app import app, db_init


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message="An error has occureds", status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# @app.errorhandler(404)
# def not_found():
#     return "Not Found", 404
#
#
# @app.errorhandler(500)
# def internal_server_error():
#     db_init.session.rollback()
#     return "Internal Server Error", 500
#

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
