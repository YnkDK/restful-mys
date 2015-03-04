from types import FunctionType

from flask import Flask
from flask.ext import restful


class Core(object):
    def __init__(self, config={}, logger=None):
        """
        Initializes the API with the given config and an optional logger

        :param config: Config dictionary available for all controllers.
                       Flask specific config can be set, see http://flask.pocoo.org/docs/0.10/config/
                       defaults to {} if not provided
        :param logger: A function like, def log_exception(sender, exception, **extra): pass, defaults to None if not
                       provided.
        """
        app = Flask(__name__)
        self.config = config

        # Set flask app config
        flask_config = set(app.config.keys())
        for cfg in config.keys():
            if cfg in flask_config:
                app.config[cfg] = config[cfg]


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

        # Set the logger if given
        if isinstance(logger, FunctionType):
            var_names = logger.func_code.co_varnames
            if var_names == ('sender', 'exception', 'extra'):
                from flask import got_request_exception

                got_request_exception.connect(logger, app)
                if app.debug:
                    print 'Connected exception logger'

        self._app = app

        # Create API and add resources
        self._api = restful.Api(self._app, catch_all_404s=True)

    def add_resource(self, controller, model, *urls, **kwargs):
        """Adds a controller to the api.

        :param controller: the class name of your controller
        :type controller: :class:`Resource`
        :param model: the class name of your model
        :type model: :class:`Model`
        :param urls: one or more url routes to match for the controller, standard
                     flask routing rules apply.  Any url variables will be
                     passed to the controller method as args.
        :type urls: str

        :param endpoint: endpoint name (defaults to :meth:`Resource.__name__.lower`
            Can be used to reference this route in :class:`fields.Url` fields
        :type endpoint: str

        Additional keyword arguments not specified above will be passed as-is
        to :meth:`flask.Flask.add_url_rule`.

        Examples::

            api.add_resource(HelloWorld, '/', '/hello')
            api.add_resource(Foo, '/foo', endpoint="foo")
            api.add_resource(FooSpecial, '/special/foo', endpoint="foo")

        """
        controller.CONFIG = self.config
        model.CONFIG = self.config
        controller.MODEL = model
        self._api.add_resource(controller, *urls, **kwargs)

    @property
    def get_app(self):
        """
        Get access to the Flask application
        :return: The application
        """
        return self._app

    def run(self, host=None, port=None, debug=None, **options):
        """Runs the application on a local development server.  If the
        :attr:`debug` flag is set the server will automatically reload
        for code changes and show a debugger in case an exception happened.

        If you want to run the application in debug mode, but disable the
        code execution on the interactive debugger, you can pass
        ``use_evalex=False`` as parameter.  This will keep the debugger's
        traceback screen active, but disable code execution.

        .. admonition:: Keep in Mind

           Flask will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to `True` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.

        .. versionchanged:: 0.10
           The default port is now picked from the ``SERVER_NAME`` variable.

        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
                     have the server available externally as well. Defaults to
                     ``'127.0.0.1'``.
        :param port: the port of the webserver. Defaults to ``5000`` or the
                     port defined in the ``SERVER_NAME`` config variable if
                     present.
        :param debug: if given, enable or disable debug mode.
                      See :attr:`debug`.
        :param options: the options to be forwarded to the underlying
                        Werkzeug server.  See
                        :func:`werkzeug.serving.run_simple` for more
                        information.
        """
        self._app.run(host, port, debug, **options)