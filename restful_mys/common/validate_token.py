import time
from os import urandom

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


def validate_token(token, secret_key):
    """
    Validates any given token. If auto_token is available in the token data and set to True and the token is valid
    the method also generates a new token with existing data in it

    :param token: Token to be validated
    :param secret_key: The secret key used to initialize the Serializer
    :return: HTTP_STATUS_CODE, data, token (new/old)
    :rtype: tuple
    """
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return 408, None, None
    except BadSignature:
        return 401, None, None
    # A 3 bytes of random numbers to scramble the token. This is useful when when a user makes multiple request
    # in a short time period.
    data['_r'] = urandom(3).encode('base-64')
    if 'auto_token' in data and data['auto_token']:
        try:
            s = Serializer(secret_key, expires_in=data['expires_in'])
            data['expires_in'] = data['expires_in']
            data['expires_at'] = int(data['expires_in'] + time.time())
        except KeyError:
            s = Serializer(secret_key, expires_in=600)
            data['expires_in'] = 600
            data['expires_at'] = int(600 + time.time())
        token = s.dumps(data)
    return 200, data, token