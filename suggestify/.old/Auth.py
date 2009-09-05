from geosuggestions import Geosuggestions

# fix me...be more better about redir urls...
    
class LoginHandler (Geosuggestions) :
    
    def get (self) :

        if self.check_logged_in() :
            self.redirect("/")

        self.do_flickr_auth(self.min_perms, '/')
        return

class LogoutHandler (Geosuggestions) :

    def post (self) :

        if not self.check_logged_in() :
            self.redirect("/")

        crumb = self.request.get('crumb')

        if not crumb :
            self.redirect("/")
            
        if not self.validate_crumb(self.user, "logout", crumb) :
            self.redirect("/")

        self.response.headers.add_header('Set-Cookie', 'ffo=')
        self.response.headers.add_header('Set-Cookie', 'fft=')    
        
        self.redirect("/")    
