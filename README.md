# RESTful by MYS
This is my little hobby project in attempting to implement a RESTful service.

It uses a Model-View-Controller-Acquaintance architecture, although the View-part is embedded in the Controller, since,
as for now, the service returns json content. The API communicates with the Controller, which processes data via the
model. Both the Controller and Model can use the classes, methods and constants defined in the Acquaintances (common).

The implementation relies greatly on [flask](http://flask.pocoo.org/) and 
[Flask-RESTful](https://github.com/flask-restful/flask-restful) and is implemented solely in Python 2.7.3. A good thing
IMHO about Python is: It is fast to develop stuff in it. But Python is slow? If you have some heavy tasks (high
CPU/memory usage) you can relatively easy implement single methods in C/C++ and transparently call these functions from
Python (and I will do this when time allows).

## Core
The core are responsible for presenting the application programming interface (API). This is where all exception
handling, registering of controllers (and therefore routes) and preparing the headers. Running [core.py](core.py) (no 
arguments) starts the application in debug mode. This is also the file to be registered with for example wsgi.

## Controller
All controller classes should only have methods named: get, post, delete,... Every data processing should be handled
via a corresponding model. All methods should return a jsonified object, i.e. a Resource should use jsonify from flask
(see [hello_world.py](restful_mys/controller/hello_world.py)) and a SecureResource (see [SecureResource](#SecureResource))
should use self.jsonify (see [secure_hello_world.py](restful_mys/controller/secure_hello_world.py)).

### SecureResource 

## Model

## Common