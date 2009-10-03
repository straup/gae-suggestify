import suggestify
import config
import md5

# TO DO (MAYBE) : nonce and/or timestamp?

class Request (suggestify.Request) :

  def __init__ (self, uuid, min_perms='read') :
    
    suggestify.Request.__init__(self, min_perms)

  def ensure_config (self, uuid) :

    if not config.robots.has_key(uuid) :
      return False
    
    self.config = config.robots[uuid]
    self.uuid = uuid
    
    return True
  
  def ensure_required_args (self, required) :

    for r in required :

      if not self.request.get(r) or self.request.get(r) == '' :
        return False

    return True

  def ensure_robot_sig (self, sig_args, robot_sig) :
    
    if robot_sig == '' :
      return False

    robot_args = self.collect_robot_args(sig_args)
    test_sig = self.generate_robot_sig(robot_args)

    if robot_sig != test_sig :
      return False
  
    return True

  def collect_robot_args (self, keys) :

    args = {}
    
    for nm in keys :
      args[ nm ] = self.request.get(nm)

    return args
  
  def generate_robot_sig (self, args) :

    raw = []
    
    keys = args.keys()
    keys.sort()
  
    for nm in keys :
      raw.append("%s=%s" % (nm, args[nm]))
      
    raw.append("_secret=%s" % self.config['signing_secret'])
    return md5.new("&".join(raw)).hexdigest()
        
  def error (self, reason='') :
    self.assign("error", reason)
    self.display("robots_error.html")
