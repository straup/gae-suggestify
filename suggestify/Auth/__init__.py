import suggestify

class TokenDance (suggestify.Request) :
  def get (self):  
    if not self.do_token_dance() :
      self.response.out.write('Ack! Flickr Auth Token dance failed.')

class Signin (suggestify.Request) :
    
    def get (self) :
        if self.check_logged_in(self.min_perms) :
            self.redirect("/")
            
        self.do_flickr_auth(self.min_perms, '/')
        return

class Signout (suggestify.Request) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.redirect("/")

        self.display("signout.html")
        return
    
    def post (self) :

        if not self.check_logged_in(self.min_perms) :
            self.redirect("/")

        crumb = self.request.get('crumb')

        if not crumb :
            self.redirect("/")
            
        if not self.validate_crumb(self.user, "logout", crumb) :
            self.redirect("/")

        self.response.headers.add_header('Set-Cookie', 'ffo=')
        self.response.headers.add_header('Set-Cookie', 'fft=')    
        
        self.redirect("/")
