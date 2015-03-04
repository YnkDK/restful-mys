from flask import jsonify as to_json, request
from flask.ext.restful import Resource, reqparse, abort

from ..common.validate_token import validate_token


class SecureResource(Resource):
    """
    A Resource which only allows access with a valid token.

    Upon initialization this class sets the following instance variables:
        request_parser: Used to add constraints, help message etc. on request parameters
        request: The request object defined in Flask, e.g. self.request.remote_addr returns the callees IP-address
        _token: The token to be returned in the response. Should never be altered
        token_data: The data saved in the original request token

    Note: The controller which extends the SecureResource can do further validations, e.g. asking the model if the
          valid token was the newest token issued.
    """

    def __init__(self, secret_key):
        """
        :param secret_key: The secret key for the app
        :type secret_key: str
        Verifies the token given as argument. Sets the following instance variables:
            token_data: The data contained in the token
            _token: The token to be returned to the user. If new_token is True, the
                   token is then renewed.
            request_parser: flask.ext.restful request parser
        """
        super(SecureResource, self).__init__()

        request_parser = reqparse.RequestParser()
        request_parser.add_argument(
            name='token',
            required=True,
            type=str,
            help="Needs argument: 'token' to access a secure resource"
        )
        request_parser.add_argument(
            name='new_token',
            required=False,
            default=False,
            type=bool,
            help='If set to true, a new token will be issued'
        )

        args = request_parser.parse_args()
        # Validate token
        status, data, token = validate_token(args['token'], secret_key)
        if status != 200:
            # Abort if token was unacceptable (expired/invalid)
            abort(status)
        # Otherwise: Set the instance variables
        self.token_data = data
        self._token = token
        self.request_parser = request_parser
        self.request = request

    def jsonify(self, *args, **kwargs):
        """
        Creates a Response with the JSON representation of the given arguments with an application/json mimetype.
        The arguments to this function are the same as to the dict constructor.

        :return: Response with JSON representation.
        """
        data = dict(*args, **kwargs)
        data['token'] = self._token
        data['expires_at'] = self.token_data['expires_at']

        return to_json(data)