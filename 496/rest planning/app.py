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
            boat_exists = False
            for item in boat.query():
                if item.id == id:
                    boat_exists = True
                    b = ndb.Key(urlsafe=id).get()
                    b_d = b.to_dict()
                    b_d['self'] = "/boat/" + id
                    self.response.write(json.dumps(b_d))
            if not boat_exists:
                self.response.status = 400
                self.response.write("error: boat does not exist")
        else:
            get_all_boats = [get_boat_query.to_dict()
                    for get_boat_query in boat.query()]
            for item in get_all_boats:
                item['self'] = "/boat/" + str(item['id'])
            self.response.write(json.dumps(get_all_boats))

    def delete(self, id=None):
        if id: 
            for item in boat.query():
                if item.id == id:
                    for space in slip.query(slip.current_boat == id):
                        slip.current_boat = ""
                        slip.arrival_date = none
                        slip.put()
                    ndb.Key(urlsafe=id).delete()
                    self.response.write("deleted boat")
        else:
            self.response.status = 400
            self.response.write("error: boat does not exist")

    def patch(self, id=None):
        if id:
            patch_boat_data = json.loads(self.request.body)
            exists = False
            for item in boat.query():
                if boat.id == id:
                    exists = True
            if exists:
                patch_boat = ndb.Key(urlsafe=id).get()
                for item in patch_boat_data:
                    if item == "name":
                        patch_boat.name = patch_boat_data['name']
                        patch_boat.put()
                        self.response.write("boat name was updated")
                    elif item == "type":
                        patch_boat.type = patch_boat_data['type']
                        patch_boat.put()
                        self.response.write("boat type was updated")
                    elif item == "length":
                        patch_boat.length = patch_boat_data['length']
                        patch_boat.put()
                        self.response.write("boat length was updated")
                    else:
                        self.response.status = 400
                        self.response.write("error: incorrect format")
            else:
                self.response.status = 400
                self.response.write("error: boat does not exist")

#define slip per reqs
class slip(ndb.Model):
    id = ndb.StringProperty()
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty()
    arrival_date = ndb.StringProperty()

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
            exists = False
            for item in slip_query_results:
                if item['number'] == slip_data['number']:
                    exists = True
                    self.response.status = 400
                    self.response.write("error: slip number is in use")
            if not exists:
                new_slip = slip(number=slip_data['number'])
                new_slip.put()
                new_slip.id = str(new_slip.key.urlsafe())
                new_slip.put()
                slip_dict = new_slip.to_dict()
                slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
                self.response.write(json.dumps(slip_dict))

    def get(self, id=None):
        if id:
            slip_exists = False
            for item in slip.query():
                if item.id == id:
                    slip_exists = True
                    s = ndb.Key(urlsafe=id).get()
                    s_d = s.to_dict()
                    s_d['self'] = "/slips/" + id
                    self.response.write(json.dumps(s_d))
            if not slip_exists:
                self.response.status = 400
                self.response.write("error: slip does not exist")
        else:
            get_all_slips = [get_slip_query.to_dict()
                    for get_slip_query in slip.query()]
            for item in get_all_slips:
                item['self'] = "/slips/" + str(item['id'])
            self.response.write(json.dumps(get_all_slips))

    def delete(self, id=None):
        if id: 
            for item in slip.query():
                if item.id == id:
                    if item.current_boat:
                        boat_in_slip = ndb.Key(urlsafe=item.current_boat).get()
                        boat_in_slip.at_sea = True;
                        boat_in_slip.put()
                    ndb.Key(urlsafe=id).delete()
                    self.response.write("deleted slip")
        else:
            self.response.status = 400
            self.response.write("error: slip does not exist")

    def patch(self, id=None):
        if id:
            patch_slip_data = json.loads(self.request.body)
            #check to see if slip id exists
            exists = False
            for item in slip.query():
                if item.id == id:
                    exists = True
            
            #self.response.write(patch_slip_data["number"])

            if exists:
                modify_slip = ndb.Key(urlsafe=id).get()
                
                #check to see if number is in use
                slip_list = [get_slip_query.to_dict()
                        for get_slip_query in slip.query()]
                num_exists = False
                for item in slip_list:
                    if item['number'] == patch_slip_data['number']:
                        num_exists = True
                        self.response.status = 400
                        self.response.write("error: slip number already exists")
                if not num_exists:
                    modify_slip.number = patch_slip_data['number']
                    modify_slip.put()
                    self.response.write("updated slip number")
            else:
                self.response.status = 400
                self.response.write("slip does not exist")


class boatsliphandler(webapp2.RequestHandler):
    def patch(self, id=None):
        if id:
            boat_data = json.loads(self.request.body)
            #check to see if boat exists
            exists = False
            for item in boat.query():
                if item.id == id:
                    exists = True
                    modify_boat = ndb.Key(urlsafe=id).get()
            if exists:
                if modify_boat.at_sea:
                    #get list of slips and find available one
                    slip_list = [get_slip_query.to_dict()
                            for get_slip_query in slip.query()]
                    empty_slip = False
                    for item in slip_list:
                        if item['current_boat'] is None:
                            empty_slip = True
                            get_slip = ndb.Key(urlsafe=item['id']).get()
                    if empty_slip:
                        get_slip.current_boat = id
                        get_slip.arrival_date = boat_data['date']
                        get_slip.put()
                        modify_boat.at_sea = False
                        modify_boat.put()
                        self.response.write("boat added to slip")
                    else:
                        self.response.status = 403
                        self.response.write("all slips are full")
                else:
                    self.response.status = 400
                    self.response.write("boat is already in a slip")
            else:
                self.response.status = 400
                self.response.write("boat does not exist")

    def delete(self, id=None):
        if id:
            exists = False
            for item in boat.query():
                if item.id == id:
                    exists = True
                    modify_boat = ndb.Key(urlsafe=id).get()
            if exists:
                if not modify_boat.at_sea:
                    slip_list = [get_slip_query.to_dict()
                                for get_slip_query in slip.query()]
                    for item in slip_list:
                        if item['current_boat'] == id:
                            get_slip = ndb.Key(urlsafe=item['id']).get()
                    get_slip.current_boat = ""
                    get_slip.arrival_date = ""
                    get_slip.put()
                    modify_boat.at_sea = True
                    modify_boat.put()
                    self.response.write("boat put at sea, slip is now empty")
                else:
                    self.response.status = 403
                    self.response.write("boat is already at sea")
            else:
                self.response.status = 403
                self.response.write("boat does not exist")


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
    ('/boat/(.*)/slip', boatsliphandler),
    ('/boat/(.*)', boathandler),
    ('/slips', sliphandler),
    ('/slips/(.*)', sliphandler),
    ], debug=True)
# [END app]
