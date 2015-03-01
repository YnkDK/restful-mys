from distutils.core import setup

setup(
    name='restful-mys',
    version='15.03',
    packages=['restful_mys', 'restful_mys.model', 'restful_mys.common', 'restful_mys.common.data',
              'restful_mys.controller'],
    url='https://github.com/YnkDK/restful-mys',
    license='MIT',
    author='Martin Storgaard',
    author_email='mys@theg33kpalace.dk',
    description='A RESTful web service',
    requires=['flask', 'flask-restful', 'psycopg2', 'bcrypt']
)
