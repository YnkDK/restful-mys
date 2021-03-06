from os import urandom

import restful_mys.core as core
from controller.hello_world import HelloWorld as HelloWorldController
from model.hello_world import HelloWorld as HelloWorldModel
from restful_mys.controller.auth import Auth as AuthController
from restful_mys.model.auth import Auth as AuthModel


cfg = {
    # Must be False when in production
    'DEBUG': True,
    # This invalidates all old tokens, which might or might not be a wanted feature
    'SECRET_KEY': urandom(24).encode('hex'),
    # Currently generated by: http://goo.gl/G17KGR
    'SALT': 'RCrf2IgHdb2gVhjm8S6O0g649dZ2X3f8SFQKZCBpc0hevycJVkiYgImCLvDS',
    # PostgreSQL databases. The table 'auth' must be in the 'default' database
    'PG_DB': {
        'default': {
            'database': 'restful',
            'user': 'mys',
            'password': 'SecurePassword',  # Please use a stronger password in production environment
            'host': 'localhost',
            'port': 5432,
            'connection_factory': None,
            'cursor_factory': None,
            'async': False,
            'autocommit': True
        }
    }
}

api = core.Core(config=cfg)
api.add_resource(AuthController, AuthModel, '/auth')
api.add_resource(HelloWorldController, HelloWorldModel, '/')

api.run()