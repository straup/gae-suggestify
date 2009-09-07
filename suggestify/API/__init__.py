import APIApp

import suggestify
import suggestify.Suggestion as Suggestion

class Request (suggestify.Request, APIApp.APIApp) :

  def __init__ (self) :
    
    suggestify.Request.__init__(self)    
    APIApp.APIApp.__init__(self)
    
  def get (self) :

    self.api_error(404, 'Method not found')
    return
  
  def post (self) :
  
    if not self.check_logged_in(self.min_perms) :
      self.api_error(403, 'Insufficient permissions')
      return

    self.run()
    return

  def run (self) :

    self.api_error(404, 'Undefined method')
    return
  
  def ensure_crumb (self, path) :

    if not self.validate_crumb(self.user, path, self.request.get('crumb')) :
      self.api_error(403, 'Invalid permissions')
      return False

    return True

  # does this really need to be here?
  
  def fetch_pending_suggestion (self, suggestion_id) :

    suggestion = Suggestion.fetch_pending_suggestion(suggestion_id)
    
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
