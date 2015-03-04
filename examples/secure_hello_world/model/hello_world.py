import random
from os.path import abspath

from restful_mys.model.model import Model


class HelloWorld(Model):
    """ A passive model structure. If
        the controller needs information
        or wants to update the database
        it have to ask the model. It is
        not notified.
    """

    def __init__(self):
        """
        Setup the Model, i.e. prepare CSV etc.
        """
        super(HelloWorld, self).__init__()
        self.pg_connect('default', self.CONFIG['PG_DB']['default'])

    def get_random_name(self):
        """
        Loads a list of unisex names and chooses a random name
        :return: A random unisex name
        :rtype: str
        """
        # List of all allowed unisex names in Denmark
        self.csv_add('names', abspath('data/names.csv'))
        # Get all names
        names = [x for x in self.csv_read('names')]
        # Clean up
        self.csv_remove('names')
        # Return a random name
        return random.choice(names)[0]
