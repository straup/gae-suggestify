import suggestify

class AboutHandler (suggestify.Request) :

    def get (self) :

        self.check_logged_in(self.min_perms)
        
        self.display("about.html")
        return
