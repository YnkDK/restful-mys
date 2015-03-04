import urllib2
import json

response = urllib2.urlopen('http://localhost:5000/')

assert response.code == 200
assert response.info()['connection'] == 'close'
assert response.info()['pragma'] == 'no-cache'
assert response.info()['cache-control'] == 'no-cache, no-store, max-age=0'
assert response.info()['content-type'] == 'application/json; charset=utf-8'
print 'Headers are as expected, content:\n{:s}'.format(json.load(response)['message'])

data = json.load(urllib2.urlopen('http://localhost:5000/?name=MYS'))  
if 'message' in data and data['message'] == 'Hello MYS!':
    print "Successfully got: '{:s}'".format(data['message'])
