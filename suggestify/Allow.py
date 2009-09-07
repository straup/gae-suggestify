import suggestify
import FlickrApp.User.Membership as Membership

class AllowHandler (suggestify.Request) :
  
  def get (self) :

    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth(self.min_perms)
      return

    crumb = self.generate_crumb(self.user, "optin")
    self.assign("optin_crumb", crumb)

    self.assign('has_opted_out', Membership.has_user_opted_out(self.user.nsid))
    self.display("allow.html")

  def post (self) :

    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth(self.min_perms)
      return

    if not self.validate_crumb(self.user, 'optin', self.request.get('crumb')) :
      self.assign('error', 'bad_crumb');
      self.display('deny.html')
      return

    if not Membership.has_user_opted_out(self.user.nsid) :
      self.assign('done', 1)
      self.display('allow.html')
      return
    
    if not self.request.get('confirm') :
      self.assign('error', 'no_confirm')
      self.display('allow.html')
      return

    # Again ... this is stupid
    self.set_opt_out(False)

    self.assign('done', 1)
    self.display('allow.html')    
