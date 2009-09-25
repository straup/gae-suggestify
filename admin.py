#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

import suggestify.Admin

if __name__ == '__main__':

  # It's like writing header files for web apps or something...
  
  handlers = [

    ('/admin/', suggestify.Admin.IndexHandler),
  ]
  
  application = webapp.WSGIApplication(handlers, debug=True)
  wsgiref.handlers.CGIHandler().run(application)
