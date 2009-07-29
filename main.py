#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

from geosuggestions.Main import MainHandler
from geosuggestions.Frob import FrobHandler
from geosuggestions.Chooser import ChooserHandler
from geosuggestions.Blocked import BlockedHandler
from geosuggestions.Review import ReviewHandler
from geosuggestions.Allow import AllowHandler
from geosuggestions.Deny import DenyHandler
from geosuggestions.Auth import LogoutHandler, LoginHandler
from geosuggestions.About import AboutHandler
from geosuggestions.Random import RandomHandler
from geosuggestions.Settings import SettingsHandler, NotificationsHandler, EmailNotificationsConfirmHandler
from geosuggestions.API import APIHandler

if __name__ == '__main__':

  handlers = [
    ('/', MainHandler),
    ('/signout', LogoutHandler),
    ('/signin', LoginHandler),    
    ('/auth', FrobHandler),
    (r'/chooser(?:/(user|photo|random)(?:/(.*))?)?', ChooserHandler),
    (r'/review(?:/(\d+))?', ReviewHandler),
    (r'/review(?:/(page\d+))?', ReviewHandler),    
    ('/blocked', BlockedHandler),    
    ('/allow', AllowHandler),
    ('/deny', DenyHandler),
    ('/api', APIHandler),
    ('/about', AboutHandler),
    ('/settings', SettingsHandler),
    ('/settings/notifications', NotificationsHandler),  
    (r'/confirm/e/(.*)', EmailNotificationsConfirmHandler),
    ('/random', RandomHandler),
    ('/faq', AboutHandler),
  ]
  
  application = webapp.WSGIApplication(handlers, debug=True)
  wsgiref.handlers.CGIHandler().run(application)
