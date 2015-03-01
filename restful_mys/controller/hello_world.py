from flask.ext import restful
from flask.ext.restful import reqparse
from flask import jsonify

from ..model.hello_world import HelloWorld as Model


class HelloWorld(restful.Resource):
    def __init__(self):
        """
        Parses the 'name' argument and sets up the model
        """
        super(HelloWorld, self).__init__()

        rp = reqparse.RequestParser()
        # Add argument
        rp.add_argument(
            name='name',
            default='',
            required=False,
            type=str,
            help='Name of the one to greet. Default: Random unisex name'
        )
        # Parse given arguments
        self.args = rp.parse_args()

        self.model = Model()

    def get(self):
        """
        Gets a Hello. If 'name' was an argument, greet the name, otherwise a random name is retrieved from
        the model
        :return: A Hello World message
        """
        if self.args['name'] == '':
            name = self.model.get_random_name()
        else:
            name = self.args['name']
        return jsonify({'message': 'Hello {:s}!'.format(name)})
