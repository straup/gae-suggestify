import suggestify
import suggestify.Suggestion as Suggestion

class ApprovedHandler (suggestify.Request) :

  def __init__ (self) :
    Geosuggestions.__init__(self, 'write')

  def get (self) :
    
    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth(self.min_perms)
      return

    approved = Suggestion.approved_suggestions_for_user(self.user.nsid)

    # please to put me in a pagination function...
    
    limit = 20
    offset = 0

    page = self.request.get('page')

    if page :
      offset = (page - 1) * limit

    #

    self.assign('count_approved', approved.count())
    self.assign('approved', approved.fetch(limit, offset))
    
    self.display('approved.html')
    return
