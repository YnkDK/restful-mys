from restful_mys.controller.secure_resource import SecureResource


class HelloWorld(SecureResource):
    def __init__(self):
        """
        Parse optional parameters and set model instance.
        """
        super(HelloWorld, self).__init__(self.CONFIG['SECRET_KEY'])
        # Initialize the model
        self.model = self.MODEL()

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