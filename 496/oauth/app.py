from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import webapp2
import urllib
import random
import string
import json
import os

CLIENT_ID = '308449516790-6j0f954v4j4rcggnbesda06pme6cbiln.apps.googleusercontent.com'
CLIENT_SECRET = '_FQyulNpzTTPLMDsFVaH9TI5'
REDIRECT = 'http://marine-waters-192703.appspot.com/authorization'

class index(webapp2.RequestHandler):
    def get(self):

class oAuth(webapp2.RequestHandler):
    def get(self):

app = webapp2.WSGIApplication([
    ('/', index),
    ('/authorization', oAuth)
], debug=True)



