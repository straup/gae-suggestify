import suggestify
import config

class Request (suggestify.Request) :

  def __init__ (self, uuid, min_perms='read') :
    
    suggestify.Request.__init__(self, min_perms)

    self.uuid = uuid
    self.config = config.robots[uuid]
    
  def ensure_required_args (self, required) :

    for r in required :

      if not self.request.get(r) or self.request.get(r) == '' :

        self.error()
        return False

    return True

  def ensure_sig (self) :

    sig = self.request.get('sig')

    if sig == '' :
      self.error()
      return False
      
    test = self.generate_sig()

    if sig != test :
      self.error()
      return False
  
    return True

  def generate_sig (self) :

    secret = self.config['signing_secret']
    
  def error (self) :
    self.response.error(403)
    
