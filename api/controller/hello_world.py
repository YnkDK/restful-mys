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
			default = "World",
			required = False,
			type = str,
			help = 'Name of the one to greet. Default: World'			
		)
		# Parse given arguments
		self.args = rp.parse_args()
		
		self.model = Model()
	
	def get(self):
		""" Greets the requester
		"""
		gretee = self.args['name']
		return jsonify({'message': 'Hello {:s}!'.format(gretee)})
