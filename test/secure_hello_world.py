import urllib2
import urllib
import json

data = urllib.urlencode({
    'login': 'mys',
    'password': 'mypassword'
})
data = json.load(urllib2.urlopen('http://localhost:5000/auth', data))

assert data['message'] == 'OK'
assert 'token' in data
assert 'expires_at' in data

print 'Login successful!'

query = urllib.urlencode({
    'token': data['token']
})
response = json.load(urllib2.urlopen('http://localhost:5000/?{:s}'.format(query)))

assert 'token' in response
assert 'expires_at' in response
assert response['token'] != data['token']
assert len(response['token']) == len(data['token'])
print 'Response message', response['message']

print '\nTesting incorrect user/password:'
data = urllib.urlencode({
    'login': 'mys',
    'password': 'hax0r'
})
try:
    data = json.load(urllib2.urlopen('http://localhost:5000/auth', data))
except urllib2.HTTPError as e:
    print 'Rejected incorrect password'

data = urllib.urlencode({
    'login': 'hax0r',
    'password': 'mypassword'
})

try:
    data = json.load(urllib2.urlopen('http://localhost:5000/auth', data))
except urllib2.HTTPError as e:
    print 'Rejected incorrect user'

data = urllib.urlencode({
    'login': 'hax0r',
    'password': 'hax0r'
})
try:
    data = json.load(urllib2.urlopen('http://localhost:5000/auth', data))
except urllib2.HTTPError as e:
    print 'Rejected incorrect user and password'


