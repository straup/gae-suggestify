import suggestify
import re
import urlparse

import FlickrApp.User as User
import FlickrApp.User.Membership as Membership
import FlickrApp.User.Blocked as Blocked

from django.utils import simplejson

class ChooserHandler (suggestify.Request) :

  def get (self, context, filter) :

    min_perms = self.min_perms

    if self.request.get('perms') == 'write' :
      min_perms = 'write'
  
    if not self.check_logged_in(min_perms) :
      self.do_flickr_auth(min_perms)
      return

    # this is who I am ...

    if not context and self.request.get('user') :
      context = 'user'
      filter = self.request.get('user')
      
    self.assign('context', context)
    
    # Default, choose a user
    
    if not context :
      self.display('chooser.html')
      return

    # ok, what are we trying to do...

    other_user = None
    other_username = None
      
    if context == 'user' :

      other_username = filter
  
    elif context == 'photo' :

      # magic referer glue, mostly for the Brooklyn Museum
      
      headers = self.request.headers

      if headers.has_key('Referer') :
        
        u = urlparse.urlparse(headers['Referer'])

        m = re.match(r'(?:www\.)?flickr\.com', u[1])
        
        if not m :
          self.error(404)
          return

        m = re.match(r'/photos/(?:[^/]+)/(\d+)', u[2])
        
        if m :
          filter = m.groups()[0]
        else :
          self.error(404)          
          return
      
      # end of magic glue
      
      method = 'flickr.photos.getInfo'

      args = {
        'photo_id' : filter,
        'auth_token' : self.user.token,
        }

      ttl = 60 * 60
      
      rsp = self.proxy_api_call(method, args, ttl)
      
      if not rsp or not rsp.has_key('photo') :
        self.assign('error', 'no_photo')
      elif rsp['photo'].has_key('location') :
        self.assign('error', 'already_geotagged')
      else :
        
        # this is kind of dumb in the end...
        
        spr = {
          'id': rsp['photo']['id'],
          'owner' : rsp['photo']['owner']['nsid'],
          'secret' : rsp['photo']['secret'],
          'server' : rsp['photo']['server'],
          'farm' : rsp['photo']['farm'],
          'title' : rsp['photo']['title']['_content'],
          'tags' : '',
          'datetaken' : rsp['photo']['dates']['taken'],
          'ownername' : rsp['photo']['owner']['username'],
          }

        if rsp['photo'].has_key('tags') :
          tags = map( lambda t: t['_content'], rsp['photo']['tags']['tag'])
          spr['tags'] = ' '.join(tags)
        
        json = simplejson.dumps({ 'photo' : [spr] })
        self.assign("photo_json", json)
          
        other_username = rsp['photo']['owner']['username']

        self.assign("usernsid", rsp['photo']['owner']['nsid'])
        
    elif context == 'random' :
      noidea_crumb = self.generate_crumb(self.user, 'method=noidea')
      self.assign('noidea_crumb', noidea_crumb);
    else :
      self.assign('error', 'unknown_context')

    # do some sanity checking on the user

    self.assign("username", other_username)
    
    if other_username :
      other_user = User.get_user_by_username(other_username)
      
      if other_user :
      
        if Blocked.is_user_blocked(self.user.nsid, other_user.nsid) :
          self.assign('blocked', 1)
          
        elif Membership.has_user_opted_out(other_user.nsid) :
          self.assign('optedout', 1)

        else :

          pass
        
        self.assign("other_user", other_user)
        
        #
        
    # crumbs
      
    crumb = self.generate_crumb(self.user, 'method=suggest')
    self.assign('suggest_crumb', crumb)

    # go!
    
    self.display('chooser.html')
    return
