from flask import jsonify as to_json
from flask.ext.restful import Resource, reqparse, abort

from validate_token import validate_token


class SecureResource(Resource):
    """
    A Resource which only allows access with a valid token.

    Note: The controller which extends the SecureResource can
          do further validations, e.g. asking the model if the
          valid token was the newest token issued.
    """

    def __init__(self):
        """
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
        status, data, token = validate_token(args['token'], args['new_token'])
        if status != 200:
            # Abort if token was unacceptable (expired/invalid)
            abort(status)
        # Otherwise: Set the instance variables
        self.token_data = data
        self._token = token
        self.request_parser = request_parser

    def jsonify(self, data):
        """
        Creates a flask formatted json object

        :param data: A data type in which a dictionary can be initialized from.
        :return: A flask formatted json object (including the token data).
        """
        data = dict(data)
        data['token'] = self._token
        data['expires_at'] = self.token_data['expires_at']

        return to_json(data)