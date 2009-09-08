#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

# (this is just me being snarky, please see the notes in the README...)

# from ifuckinghateyoupython import *

from suggestify.Main import MainHandler
from suggestify.Example import ExampleHandler
from suggestify.Frob import FrobHandler
from suggestify.Chooser import ChooserHandler
from suggestify.Blocked import BlockedHandler
from suggestify.Review import ReviewHandler
from suggestify.Allow import AllowHandler
from suggestify.Deny import DenyHandler
from suggestify.Auth import LogoutHandler, LoginHandler
from suggestify.About import AboutHandler
from suggestify.Prefs import PrefsHandler, NotificationsHandler, EmailNotificationsConfirmHandler

# My hate has an API...

import suggestify.API.Suggest
import suggestify.API.Approve
import suggestify.API.Reject
import suggestify.API.Block
import suggestify.API.PeopleInfo
import suggestify.API.Email
import suggestify.API.Flickr
import suggestify.API.Search

if __name__ == '__main__':

  # It's like writing header files for web apps or something...
  
  handlers = [

    ('/', MainHandler),
    ('/faq', AboutHandler),
    ('/about', AboutHandler),
    ('/example', ExampleHandler),    
    
    ('/signout', LogoutHandler),
    ('/signin', LoginHandler),    
    ('/auth', FrobHandler),

    (r'/chooser(?:/(user|photo|random)(?:/(.*))?)?', ChooserHandler),
    (r'/review(?:/(\d+))?', ReviewHandler),
    (r'/review(?:/(page\d+))?', ReviewHandler),    

    ('/allow', AllowHandler),
    ('/deny', DenyHandler),
    ('/blocked', BlockedHandler),
    
    ('/settings', PrefsHandler),
    ('/settings/notifications', NotificationsHandler),  
    (r'/confirm/e/(.*)', EmailNotificationsConfirmHandler),

    ('/api/suggest', suggestify.API.Suggest.SuggestHandler),
    ('/api/approve', suggestify.API.Approve.ApproveHandler),
    ('/api/reject', suggestify.API.Reject.RejectHandler),
    ('/api/block', suggestify.API.Block.BlockHandler),        
    ('/api/unblock', suggestify.API.Block.UnBlockHandler),
    ('/api/buddyicon', suggestify.API.PeopleInfo.BuddyiconHandler),
    ('/api/pathalias', suggestify.API.PeopleInfo.PathAliasHandler),
    ('/api/enable_email', suggestify.API.Email.EmailEnableHandler),
    ('/api/disable_email', suggestify.API.Email.EmailDisableHandler),    
    ('/api/flickr.photos.getInfo', suggestify.API.Flickr.PhotoGetInfoHandler),
    ('/api/flickr.people.getInfo', suggestify.API.Flickr.PeopleGetInfoHandler),
    ('/api/flickr.places.getInfo', suggestify.API.Flickr.PlacesGetInfoHandler),        
    ('/api/flickr.people.findByUsername', suggestify.API.Flickr.FindByUsernameHandler),        
    ('/api/search', suggestify.API.Search.SearchForUserHandler),
  ]
  
  application = webapp.WSGIApplication(handlers, debug=True)
  wsgiref.handlers.CGIHandler().run(application)
