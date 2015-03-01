from restful_mys.common.secure_resource import SecureResource
from restful_mys.controller.hello_world import HelloWorld


class SecureHelloWorld(SecureResource, HelloWorld):
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