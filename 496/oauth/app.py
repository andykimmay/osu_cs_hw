from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import webapp2
import urllib
import random
import string
import json
import os

CLIENT_ID = '308449516790-bsi5gplq6miq88ra8cpl6j4k8s98ua0h.apps.googleusercontent.com' 
CLIENT_SECRET = ' 73vRPt_qkMndrIvkybbu5OtL'
REDIRECT = 'http://trust-tiger.appspot.com/authorization'

class index(webapp2.RequestHandler):
    def get(self):

class oAuth(webapp2.RequestHandler):
    def get(self):

app = webapp2.WSGIApplication([
    ('/', index),
    ('/authorization', oAuth)
], debug=True)



