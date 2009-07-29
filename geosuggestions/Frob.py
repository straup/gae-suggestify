from geosuggestions import Geosuggestions

class FrobHandler (Geosuggestions) :

  def get (self):  

    if not self.do_token_dance() :
      self.response.out.write('SNFU')
