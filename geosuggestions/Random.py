# this is probably better served via the local API but for now...

from geosuggestions import Geosuggestions

from config import config
import Flickr.API
import random
import time

class RandomHandler (Geosuggestions) :

  def get (self) :

    if not self.check_logged_in(self.min_perms) :
      self.do_flickr_auth(self.min_perms)
      return

    sort = ['date-posted-asc',
            'date-posted-desc',
            'date-taken-asc',
            'date-taken-desc',
            'interestingness-desc',
            'interestingness-asc',
            'relevance']

    random.shuffle(sort)
    random.shuffle(sort)

    contacts = ['ff', 'all']
    random.shuffle(contacts)
    
    per_page = max(int(random.random() * 100), 25)

    prop = random.random()
    format = "%Y-%m-%d"
    stime = time.mktime(time.strptime('1970-01-01', format))
    etime = time.time()

    ptime = stime + prop * (etime - stime)

    date_taken  = time.strftime(format, time.localtime(ptime))

    args = {
      'auth_token' : self.user.token,
      'user_id' : self.user.nsid,
      'contacts' : contacts[0],
      'has_geo' : 0,
      'per_page' : per_page,
      'sort' : sort[0],
      'max_taken_date' : "%s 00:00:00" % date_taken,
      'extras' : 'owner_name,date_taken'
    }

    
    # sig = Flickr.API.sign_args(config['flickr_apisecret'], args)

    rsp = self.api_call('flickr.photos.search', args)

    print "xxx"

    print args
    print "<br />"
    
    if not rsp['photos']['photo'] :
      print "try again"
      return
    
    for ph in rsp['photos']['photo'] :
      print "'%s' by %s (%s)" % (ph['title'].encode("ascii", "ignore"), ph['ownername'].encode("ascii", "ignore"), ph['datetaken'])
      print "<br />"
    return
