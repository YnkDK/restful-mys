import random

class HelloWorld(object):
	""" A passive model structure. If
	    the controllor needs information
	    or wants to update the database
	    it have to ask the model. It is
	    not notified.
	"""
	def __init__(self, data):
		""" Sets the data object given
		    from the controller. In the
		    structure used, the data obj
		    is actually from the core, i.e.
		    we only create one connection to
		    the database per request.
		"""
		self.data = data
	
	def getRandomName(self):
		# List of all allowed unisex names in Denmark
		self.data.addCSV('names', 'data/names.csv')
		# Get all names
		names = [x for x in self.data.read('names')]
		# Clean up
		self.data.removeCSV('names')
		# Return a random name
		return random.choice(names)[0]
