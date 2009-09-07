import suggestify

class FrobHandler (suggestify.Request) :

  def get (self):  

    if not self.do_token_dance() :
      self.response.out.write('SNFU')
