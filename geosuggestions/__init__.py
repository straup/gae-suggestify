from config import config

import Flickr.API
from FlickrApp import FlickrApp
import FlickrApp.User.Membership as Membership

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
import os.path

class Geosuggestions (FlickrApp) :

  def __init__ (self, min_perms='read') :
    FlickrApp.__init__(self, config['flickr_apikey'], config['flickr_apisecret'])
    
    self.min_perms = min_perms

    self.membership = None
    self.template_values = {}

  def check_logged_in (self, min_perms=None) :

    if not FlickrApp.check_logged_in(self, min_perms) :
      return False

    membership = Membership.retrieve(self.user.nsid)

    if not membership :
      membership = Membership.create(self.user.nsid)
      
    self.membership = membership
    self.has_opted_out = membership.opted_out

    return True
      
  def assign (self, key, value) :
    self.template_values[key] = value
    
  def display (self, template_name) :

    self.assign("config", config)
    self.assign("host", self.request.host)
    self.assign("host_url", self.request.host_url)    
    self.assign("path_info", self.request.path_info)

    if self.user :
      self.assign('user', self.user)
      self.assign('logout_crumb', self.generate_crumb(self.user, "logout"))
      
    root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root, 'templates', template_name)

    self.response.out.write(template.render(path, self.template_values))

  def set_opt_out (self, opt_out=True) :

    if opt_out :
      return Membership.opt_out(self.membership)

    return Membership.opt_in(self.membership)    

  def default_geoperms (self) :
    method = 'flickr.prefs.getGeoPerms'
    args = {'auth_token' : self.user.token}                 
    ttl = 14
        
    rsp = self.proxy_api_call(method, args, ttl)
    return rsp['person']['geoperms']

  def filter_spr (self, spr ) :

    # get all the pending suggestions for the logged in user

    # get all the suggestion the user has said "dunno" for

    # get all the users the logged in user is blocked by

    # get all the user

    pass
  
  def proxy_api_call (self, method, args, ttl=0) :

    sig = Flickr.API.sign_args(method, args)
    
    memkey = "%s_%s" % (method, sig)
    cache = memcache.get(memkey)

    if cache :
      return cache

    rsp = self.api_call(method, args)

    if rsp['stat'] == 'ok' :
      memcache.add(memkey, rsp, ttl)

    return rsp
