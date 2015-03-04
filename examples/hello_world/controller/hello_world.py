from restful_mys.controller.resource import Resource


class HelloWorld(Resource):
    def __init__(self):
        """
        Parse optional parameters and set model instance.
        """
        super(HelloWorld, self).__init__()

        # Add argument
        self.request_parser.add_argument(
            name='name',
            default='',
            required=False,
            type=str,
            help='Name of the one to greet. Default: Random unisex name'
        )
        # Parse given arguments
        self.args = self.request_parser.parse_args()
        # Initialize the model
        self.model = self.MODEL()

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
        return self.jsonify({'message': 'Hello {:s}!'.format(name)})