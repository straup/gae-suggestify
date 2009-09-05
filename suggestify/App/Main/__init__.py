import suggestify
import suggestify.Suggestion as Suggestion
import FlickrApp.User.Membership as Membership

class Request (suggestify.Request)

  def get (self):

    if self.check_logged_in(self.min_perms) :

      pending = Suggestion.pending_suggestions_for_user(self.user.nsid)

      self.assign('pending_suggestions', pending.count())      
      self.assign('has_opted_out', Membership.has_user_opted_out(self.user.nsid))

    self.display('main.html')
