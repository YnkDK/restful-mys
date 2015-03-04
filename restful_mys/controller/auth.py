import time

from flask.ext.restful import Resource, reqparse, abort
from flask import jsonify

from ..model.auth import Auth as Model
from restful_mys.controller.secure_resource import SecureResource


class Auth(Resource):
    def __init__(self):
        """
        Sets up request parser and model for authentication
        """
        super(Auth, self).__init__()

        self.request_parser = reqparse.RequestParser()

        self.model = Model()

    def get(self):
        """
        Checks if a token is valid.

        :return: OK if token was valid, Unauthorized if invalid or Request Timeout if expired
        """
        sr = SecureResource(self.CONFIG['SECRET_KEY'])
        return sr.jsonify({'message': 'OK'})

    def post(self):
        """
        A typical login scenario. If login/password combination is correct, a token is generated which would be a key
        for all SecureResources. If login/password combination is invalid then 'Unauthorized' is returned.
        :return:
        """
        self.request_parser.add_argument(
            name='login',
            required=True,
            type=str,
            help="Needs argument: 'login' - the user login"
        )
        self.request_parser.add_argument(
            name='password',
            required=True,
            type=str,
            help="Needs argument: 'password' - the user password"
        )
        self.request_parser.add_argument(
            name='expire',
            required=False,
            default=600,
            type=int,
            help="Argument: 'expire' - the time (seconds) the issued token should be valid. Default to 600 seconds."
        )
        args = self.request_parser.parse_args()

        # Check login and issue token
        login_id, token = self.model.validate_login(args['login'], args['password'], args['expire'])
        if login_id is None:
            # Unauthorized access
            abort(401)

        return jsonify({
            'message': 'OK',
            'token': token,
            'expires_at': int(time.time() + args['expire'])
        })