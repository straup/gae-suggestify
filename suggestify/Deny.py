import suggestify
import suggestify.Suggestion as Suggestion
import FlickrApp.User.Membership as Membership

class DenyHandler (suggestify.Request) :

  def get (self) :

    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth(self.min_perms)
      return

    crumb = self.generate_crumb(self.user, "optout")
    self.assign("optout_crumb", crumb)
    
    self.assign('has_opted_out', Membership.has_user_opted_out(self.user.nsid))
    self.display("deny.html")

  def post (self) :
    
    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth()
      return

    if not self.validate_crumb(self.user, 'optout', self.request.get('crumb')) :
      self.assign('error', 'bad_crumb');
      self.display('deny.html')
      return

    if Membership.has_user_opted_out(self.user.nsid) :
      self.assign('done', 1)
      self.display('deny.html')
      return
    
    if not self.request.get('confirm') :
      self.assign('error', 'no_confirm')
      self.display('deny.html')
      return

    Membership.opt_out(self.user.nsid)
    
    Suggestion.reject_all_pending_suggestions_for_owner(self.user.nsid)
    
    self.assign('done', 1)
    self.display('deny.html')
