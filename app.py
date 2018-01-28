#!/usr/bin/env python

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json

#define boat per assignment reqs
class boat(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    b_type = ndb.StringProperty(required=True)
    length = ndb.StringProperty(required=True)
    at_sea = ndb.BooleanProperty()

#define boat handler
class boathandler(webapp2.RequestHandler):
    #create boat
    def post(self):
        boat_data = json.loads(self.request.body)
        #must have required fields to create boat
        if not all([boat_data.get('name'), 
            boat_data.get('b_type'), 
            boat_data.get('length')]):
            self.response.status = 400
            self.response.write("error: cannot create boat, need all required fields")
        else:    
            new_boat = boat(name=boat_data['name'],
                    b_type=boat_data['b_type'],
                    length=boat_data['length'],
                    at_sea=True)
            new_boat.put()
            new_boat.id = str(new_boat.key.urlsafe())
            new_boat.put()
            boat_dict = new_boat.to_dict()
            boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
            self.response.write(json.dumps(boat_dict))

    def get(self, id=None):
        if id:
            for item in boat.query():
                if item.id == id:
                    b = ndb.Key(urlsafe=id).get()
                    b_d = b.to_dict()
                    b_d['self'] = "/boat/" + id
                    self.response.write(json.dumps(b_d))
                else:
                    self.response.status = 400
                    self.response.status.write("error: boat does not exist")
        else:
            get_all_boats = [get_boat_query.to_dict()
                    for get_boat_query in boat.query()]
            for item in get_all_boats:
                item['self'] = "/boat/" + str(item['id'])
            self.response.write(json.dumps(get_all_boats))

#define slip per reqs
class slip(ndb.Model):
    id = ndb.StringProperty()
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty()
    arrival_date = ndb.DateProperty()

#define slip handler
class sliphandler(webapp2.RequestHandler):
    def post(self):
        slip_data = json.loads(self.request.body)
        slip_query_results = [slip_query.to_dict()
                            for slip_query in slip.query()]
        #must have required fields to create slip
        if not slip_data.get('number'):
            self.response.status = 400
            self.response.write("error: cannot create slip, need all required fields")
        else:    
            for item in slip_query_results:
                if item['number'] == slip_data['number']:
                    self.response.status = 401
                    self.response.write("error: slip number is in use")
                else:
                    new_slip = slip(number=slip_data['number'])
                    new_slip.put()
                    new_slip.id = str(new_slip.key.urlsafe())
                    new_slip.put()
                    slip_dict = new_slip.to_dict()
                    slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
                    self.response.write(json.dumps(slip_dict))
    
    def get(self, id=None):
        if id:
            for item in slip.query():
                if item.id == id:
                    s = ndb.Key(urlsafe=id).get()
                    s_d = s.to_dict()
                    s_d['self'] = "/slips/" + id
                    self.response.write(json.dumps(b_d))
                else:
                    self.response.status = 400
                    self.response.status.write("error: slip does not exist")
        else:
            get_all_slips = [get_slip_query.to_dict()
                    for get_slip_query in slip.query()]
            for item in get_all_slips:
                item['self'] = "/slips/" + str(item['id'])
            self.response.write(json.dumps(get_all_slips))
'''
        if id:
            s = ndb.Key(urlsafe=id).get()
            s_d = s.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.write(json.dumps(s_d))
'''
# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write("hello world")

#stackoverflow, allow for patch
#https://stackoverflow.com/questions/16280496/patch-method-handler-on-google-appengine-webapp2
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', boathandler),
    ('/boat/(.*)', boathandler),
    ('/slips', sliphandler),
    ('/slips/(.*)', sliphandler)
    ], debug=True)
# [END app]
