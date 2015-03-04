import restful_mys.core as mys
from controller.hello_world import HelloWorld as HelloWorldController
from model.hello_world import HelloWorld as HelloWorldModel
from restful_mys.controller.auth import Auth as AuthController
from restful_mys.model.auth import Auth as AuthModel

cfg = {
    # Must be False when in production
    'DEBUG': True,
    # Currently generated by: http://goo.gl/O4Ogb5
    'SECRET_KEY': 'MYpqfhw2FMRHODTGUvH7NB6KPcX4N0Q8dS0VbPfU',
    # Currently generated by: http://goo.gl/G17KGR
    'SALT': 'RCrf2IgHdb2gVhjm8S6O0g649dZ2X3f8SFQKZCBpc0hevycJVkiYgImCLvDS',
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

core = mys.Core(config=cfg)
core.add_resource(AuthController, AuthModel, '/auth')
core.add_resource(HelloWorldController, HelloWorldModel, '/')

core.run()