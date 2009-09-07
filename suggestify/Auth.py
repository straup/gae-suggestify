import suggestify
    
class LoginHandler (suggestify.Request) :
    
    def get (self) :

        if self.check_logged_in(self.min_perms) :
            self.redirect("/")

        self.do_flickr_auth(self.min_perms, '/')
        return

class LogoutHandler (suggestify.Request) :

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
