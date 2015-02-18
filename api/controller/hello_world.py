from flask.ext import restful
from flask.ext.restful import reqparse
from flask import jsonify
from model.hello_world import HelloWorld as Model

class HelloWorld(restful.Resource):
	def __init__(self):
		""" Parse request parameters.
		"""
		super(HelloWorld, self).__init__()
		
		rp = reqparse.RequestParser()
		# Add argument
		rp.add_argument(
			name = 'name',
			default = '',
			required = False,
			type = str,
			help = 'Name of the one to greet. Default: Random unisex name'			
		)
		# Parse given arguments
		self.args = rp.parse_args()
		# If the data attribute was set as
		# a class variable => use it
		self.model = Model(getattr(self, 'data', None))
	
	def get(self):
		""" Greets the requester
		"""
		if self.args['name'] == '':
			gretee = self.model.getRandomName()
		else:
			gretee = self.args['name']
		return jsonify({'message': 'Hello {:s}!'.format(gretee)})
