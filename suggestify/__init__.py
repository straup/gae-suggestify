from FlickrApp.Handlers import FlickrAppRequest
from config import config

import suggestify.Settings as Settings

from google.appengine.api import memcache

class Request (FlickrAppRequest) :
    def __init__ (self) :
        FlickrAppRequest.__init__(self, config)
                
    def check_logged_in (self, min_perms) :

        if not FlickrAppRequest.check_logged_in(self, min_perms) :
            return False

        settings = Settings.get_settings_for_user(self.user.nsid)
        self.user.settings = settings

        return True
      
  def default_geoperms (self) :

    method = 'flickr.prefs.getGeoPerms'
    args = {'auth_token' : self.user.token}                 
    ttl = 14
        
    rsp = self.proxy_api_call(method, args, ttl)
    return rsp['person']['geoperms']

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
