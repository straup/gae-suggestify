from geosuggestions.API.Core import CoreHandler
from geosuggestions.API.Echo import EchoHandler
from geosuggestions.API.Suggest import SuggestHandler
from geosuggestions.API.Approve import ApproveHandler
from geosuggestions.API.Reject import RejectHandler
from geosuggestions.API.PeopleInfo import BuddyiconHandler, PathAliasHandler
from geosuggestions.API.Block import BlockHandler, UnBlockHandler
from geosuggestions.API.Email import EmailEnableHandler, EmailDisableHandler
from geosuggestions.API.Flickr import PhotoGetInfoHandler, PeopleGetInfoHandler, FindByUsernameHandler, PlacesGetInfoHandler
from geosuggestions.API.Search import SearchForUserHandler, SearchRandomByContactsHandler
from geosuggestions.API.Random import NoIdeaHandler

import geosuggestions.Suggestion as dbSuggestion

class APIHandler (CoreHandler) :
  
  def get (self) :
    return self.error(404)
  
  def post (self) :
  
    if not self.check_logged_in(self.min_perms) :
      self.api_error(403)
      return

    method = self.request.get('method')
    format = self.request.get('format')

    if format and not format in self.valid_formats :
      self.api_error(999, 'Not a valid format')
      return

    if format :
      self.format = format

    # This is dumb.
    # There should be a better way...
     
    if method == 'echo' :
      EchoHandler().run(self)
    elif method == 'suggest' :
      SuggestHandler().run(self)
    elif method == 'approve' :
      ApproveHandler().run(self)
    elif method == 'reject' :
      RejectHandler().run(self)
    elif method == 'block' :
      BlockHandler().run(self)
    elif method == 'unblock' :
      UnBlockHandler().run(self)
    elif method == 'buddyicon' :
      BuddyiconHandler().run(self)
    elif method == 'pathalias' :
      PathAliasHandler().run(self)
    elif method == 'enable_email' :
      EmailEnableHandler().run(self)
    elif method == 'disable_email' :
      EmailDisableHandler().run(self)                  
    elif method == 'flickr.photos.getInfo' :
      PhotoGetInfoHandler().run(self)
    elif method == 'flickr.people.getInfo' :
      PeopleGetInfoHandler().run(self)
    elif method == 'flickr.people.findByUsername' :
      FindByUsernameHandler().run(self)
    elif method == 'flickr.places.getInfo' :
      PlacesGetInfoHandler().run(self)            
    elif method == 'search' :
      SearchForUserHandler().run(self)
    elif method == 'random' :
      SearchRandomByContactsHandler().run(self)
    elif method == 'noidea' :
      NoIdeaHandler().run(self)            
    else :
      self.api_error(99, 'Unknown method ' + method)
          
  def ensure_crumb (self, path) :

    if not self.validate_crumb(self.user, path, self.request.get('crumb')) :
      self.api_error(400, "OH NOES")
      return False

    return True

  def fetch_pending_suggestion (self, suggestion_id) :

    suggestion = dbSuggestion.fetch_pending_suggestion(suggestion_id)
    
    if not suggestion :
      self.api_error(5, 'Not a valid suggestion ID')
      return False

    if suggestion.owner_nsid != self.user.nsid :
      self.api_error(6, 'Not a valid suggestion')
      return False

    if suggestion.status != 1 :
      self.api_error(7, 'Suggestion has already been ...')
      return False

    return suggestion
