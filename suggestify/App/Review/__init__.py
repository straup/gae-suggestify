from geosuggestions import Geosuggestions
import geosuggestions.Suggestion as Suggestion

class ReviewHandler (Geosuggestions) :

  def __init__ (self) :
    Geosuggestions.__init__(self, 'write')

  def get (self, filter=None) :
        
    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth(self.min_perms)
      return

    #
    
    photo_id = None
    page = None

    if filter :

      if filter.startswith("page") :
        page = filter.replace("page", "")
      else :
        photo_id = filter

    #

    default = self.default_geoperms()
    self.assign("geo_perms", default)

    #
    
    pending = Suggestion.pending_suggestions_for_user(self.user.nsid, photo_id)

    # please to put me in a pagination function...
    
    limit = 20
    offset = 0

    page = self.request.get('page')

    if page :
      offset = (page - 1) * limit

    #

    self.assign('count_pending', pending.count())
    self.assign('pending', pending.fetch(limit, offset))

    approve_crumb = self.generate_crumb(self.user, 'method=approve')
    reject_crumb = self.generate_crumb(self.user, 'method=reject')
    block_crumb = self.generate_crumb(self.user, 'method=block')

    self.assign('approve_crumb', approve_crumb)
    self.assign('reject_crumb', reject_crumb)
    self.assign('block_crumb', block_crumb)
    
    self.display('review.html')
    return
