from os import urandom
import random
import hashlib
import time

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt
from flask import abort

from restful_mys.model.model import Model


class Auth(Model):
    """
    Handles all authentications of a user, i.e.
        1. Issues new passwords
        2. Validates user/password
        3. Issues new tokens
    Note that the validation of tokens is not a method
    of this class, since Secure Resources are to validate tokens.
    """

    def __init__(self):
        super(Auth, self).__init__()

        self.secret_key = self.CONFIG['SECRET_KEY']
        self.salt = self.CONFIG['SALT']

        try:
            self.pg_connect('default', self.CONFIG['PG_DB']['default'])
        except KeyError:
            abort(
                500,
                message='Internal Server Error',
                method='model.auth.__init__',
                error_message=KeyError.message
            )

    def new_password(self, login, password):
        """
        Generates an encrypted password for a given user

        :param login: Plain text user login
        :param password: Plain text user password
        :return: Encrypted login, Encrypted password
        :rtype : tuple
        """
        login = self._sha512('{:s}{:s}'.format(login, self.salt))
        pw = self._pepper_hash(self._get_peppers(login).next(), password, self.salt)
        hashed = bcrypt.hashpw(pw, bcrypt.gensalt(7))
        return login, hashed

    def validate_login(self, login, password, expire):
        """
        Validates the login/password combination with the database.

        :param login: Plain text user login
        :param password: Plain text user password
        :param expire: Time in seconds in which a token should be valid
        :return: (User ID, token) if successful, (None, None) otherwise
        :rtype: tuple
        """

        login = self._sha512('{:s}{:s}'.format(login, self.salt))
        # Select id/hashed password from database
        try:
            res = self.pg_select('id, password, auto_token', 'auth', 'login = %s', (login,)).next()
        except StopIteration:
            # Login not found
            # TODO: Sleep for some seconds here
            return None, None

        # Validate the login information given
        login_id, hashed, auto_token = res
        for pepper in self._get_peppers(login):
            # Add some pepper to the password
            pw = self._pepper_hash(pepper, password, self.salt)
            if bcrypt.hashpw(pw, hashed) == hashed:
                # The password was correct! Create token and return it.
                s = Serializer(self.secret_key, expires_in=expire)
                return login_id, s.dumps({
                    'id': login_id,
                    'expires_in': expire,
                    'expires_at': int(time.time() + expire),
                    'auto_token': auto_token,
                    '_r': urandom(3).encode('base-64')
                })
        return None, None

    @staticmethod
    def _get_peppers(login):
        """
        Constructs a list of 255 random integers specific for a given login.
        Note: This could just have been all possible numbers of a byte, i.e. 0..255

        :param login: SHA512 hash of user login
        :return: A generator
        :rtype: collections.Iterable
        """
        # Make the random sequence dependent on the user login
        random.seed(login)
        # noinspection PyUnusedLocal
        peppers = [random.randint(0, 9999999) for r in xrange(255)]

        # Jump to a request dependent state to shuffle the peppers.
        # This ensures that the shuffle is different from time to time
        random.jumpahead(int(time.time()))
        random.shuffle(peppers)

        # Yield the peppers one by one
        for pepper in peppers:
            yield pepper

    @staticmethod
    def _pepper_hash(pepper, password, salt):
        """
        Appends 8 digits in front of user password and concatenates application salt
        to the user password. In the current configuration this leaves a password of
        length 8 + length of user password + 60 - which should be plenty for a brute
        force attack. Note that bcrypt also makes a user specific salt.

        :param pepper: Any digit that should be used as pepper
        :param password: The plain text password
        :param salt: Application salt
        :return: pepper + password + application salt
        :rtype: str
        """
        return '{:0>8}{:s}{:s}'.format(pepper, password, salt)

    @staticmethod
    def _sha512(message):
        """
        Creates the SHA512 digest of the message.

        :param message: Some message
        :return: Hexadecimal SHA512 digest
        :rtype: str
        """
        return hashlib.sha512(message).hexdigest()