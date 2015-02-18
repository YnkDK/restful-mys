from config import * 
from flask import Flask
from flask.ext import restful
# Import data handler
from common.data import Data
# Import the controllers
from controller.hello_world import HelloWorld

# Initialzie app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Folder options
app.template_folder = TEMPLATE_FOLDER
app.upload_folder = UPLOAD_FOLDER

@app.after_request
def add_header(response):
	"""
	Add headers to tell the caller that it shoudn't cache the data,
	in addition the content type is set to json
	"""
	response.headers['Cache-Control'] = 'no-cache, no-store, max-age=0'
	response.headers['Connection'] = 'close'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Content-Type'] = 'application/json; charset=utf-8'

	if 'WWW-Authenticate' in response.headers:
		del response.headers['WWW-Authenticate']
	if 'X-XSS-Protection' in response.headers:
		del response.headers['X-XSS-Protection']
	if 'X-Content-Type-Options' in response.headers:
		del response.headers['X-Content-Type-Options']
	if 'Content-Security-Policy' in response.headers:
		del response.headers['Content-Security-Policy ']
	return response

# Create data object
dat = Data()

# Make data object available for classes that needs it
HelloWorld.data = dat

# Create API and add resources
api = restful.Api(app)
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
	# Run in debug mode
    app.run(debug=True)
