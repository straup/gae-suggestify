import suggestify

class ExampleHandler (suggestify.Request) :

    def get (self) :

        self.check_logged_in(self.min_perms)
        
        self.display("example.html")
        return
