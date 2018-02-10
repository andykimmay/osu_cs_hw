from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import webapp2
import urllib
import random
import string
import json
import os

CLIENT_ID = '147678634069-so1aviujnuhabbnlauqf7r6nqmostjic.apps.googleusercontent.com' 
CLIENT_SECRET = 'RfBXXDxOCKou4_3AZB4SyolJ'
REDIRECT = 'http://trust-tiger.appspot.com/authorization'

class index(webapp2.RequestHandler):
    def get(self):
        randomString = ''.join(random.choice(string.ascii_letters) for x in range(10))

        url_text = 'Click Here to Authenticate'

        url = "https://accounts.google.com/o/oauth2/v2/auth?scope=email&access_type=offline&include_granted_scopes=true&state="
        url = url + randomString
        url = url + "&redirect_uri=https://oauth2-imp.appspot.com/authorize&&response_type=code&client_id="
        url = url + CLIENT_ID

        url_value = {'url':url}

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, url_value))


app = webapp2.WSGIApplication([
    ('/', index),
], debug=True)
