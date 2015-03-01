from flask import Flask, got_request_exception
from flask.ext import restful
# Import the controllers
from restful_mys.controller.hello_world import HelloWorld
from restful_mys.controller.auth import Auth
from restful_mys.controller.secure_hello_world import SecureHelloWorld

# Initialize app
app = Flask(__name__)


@app.after_request
def add_header(response):
    """
    Add some expected RESTful headers, i.e. tell the caller that it shouldn't cache the data, and
    that the content is of type json.

    :param response: Current response
    :return: Final response
    """
    response.headers['Cache-Control'] = 'no-cache, no-store, max-age=0'
    response.headers['Connection'] = 'close'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'

    if 'WWW-Authenticate' in response.headers:
        del response.headers['WWW-Authenticate']
    if 'X-XSS-Protection' in response.headers:
        del response.headers['X-XSS-Protection']
    if 'X-Content-Type-Options' in response.headers:
        del response.headers['X-Content-Type-Options']
    if 'Content-Security-Policy' in response.headers:
        del response.headers['Content-Security-Policy ']

    return response


def log_exception(sender, exception, **extra):
    """
    Log exceptions made by the application.

    :param sender: Whom send the exception (app)
    :param exception: The exception raised
    :param extra: Any extra information bound to the exception
    """
    # TODO: Log exceptions
    print sender, exception, extra


got_request_exception.connect(log_exception, app)

# Create API and add resources
api = restful.Api(app, catch_all_404s=True)
# Add all controllers
api.add_resource(HelloWorld, '/')
api.add_resource(SecureHelloWorld, '/secure')
api.add_resource(Auth, '/auth')

if __name__ == '__main__':
    # Run in debug mode
    app.run(debug=True)
