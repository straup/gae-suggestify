import suggestify

class FrobHandler (suggestify.Request) :

  def get (self):  

    if not self.do_token_dance() :
      self.display("auth_error.html")
