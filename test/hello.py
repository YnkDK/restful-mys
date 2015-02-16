import urllib2
import json

data = json.load(urllib2.urlopen('http://localhost:5000/'))  
if 'message' in data and data['message'] == 'Hello World!':
	print "Successfully got: '{:s}'".format(data['message'])
	
data = json.load(urllib2.urlopen('http://localhost:5000/?name=MYS'))  
if 'message' in data and data['message'] == 'Hello MYS!':
	print "Successfully got: '{:s}'".format(data['message'])
