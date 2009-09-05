from geosuggestions import Geosuggestions

class AboutHandler (Geosuggestions) :

    def get (self) :

        self.check_logged_in(self.min_perms)
        
        self.display("about.html")
        return
