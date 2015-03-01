import time

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from restful_mys.common.config import SECRET_KEY


def validate_token(token, new_token=False):
    """
    Validates any given token. If new_token is True and the token is valid
    the method also generates a new token using the existing data.

    :param token: Token to be validated
    :param new_token: Boolean, if True a new token is generated
    :return: HTTP_STATUS_CODE, data, token (new/old)
    :rtype: tuple
    """
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return 408, None, None
    except BadSignature:
        return 401, None, None

    if new_token:
        try:
            s = Serializer(SECRET_KEY, expires_in=data['expires_in'])
            data['expires_in'] = data['expires_in']
            data['expires_at'] = int(data['expires_in'] + time.time())
        except KeyError:
            s = Serializer(SECRET_KEY, expires_in=600)
            data['expires_in'] = 600
            data['expires_at'] = int(600 + time.time())
        token = s.dumps(data)
    return 200, data, token