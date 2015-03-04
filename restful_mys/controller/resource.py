from flask.ext.restful import Resource as FlaskResource, reqparse
from flask import jsonify as to_json, request


class Resource(FlaskResource):
    """
    A Resource as defined in flask.ext.restful.Resource with an additional method: jsonify which is a wrapper
    function for jsonify from the flask module. This class is included, such that jsonify have same interface
    as a SecureResource.

    Upon initialization this class sets the following instance variables:
        request_parser: Used to add constraints, help message etc. on request parameters
        request: The request object defined in Flask, e.g. self.request.remote_addr returns the callees IP-address
    """

    def __init__(self):
        """
        Initializes the Flask Resource
        """
        super(Resource, self).__init__()
        self.request_parser = reqparse.RequestParser()
        self.request = request

    @staticmethod
    def jsonify(*args, **kwargs):
        """
        Creates a Response with the JSON representation of the given arguments with an application/json mimetype.
        The arguments to this function are the same as to the dict constructor.

        :return: Response with JSON representation.
        """
        return to_json(*args, **kwargs)