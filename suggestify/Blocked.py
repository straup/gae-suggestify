import suggestify

import FlickrApp.User as User
import FlickrApp.User.Blocked as Blocked

class BlockedHandler (suggestify.Request) :

    # if you're blocking people chances are good
    # you're actually accepting suggestions so let's
    # start by assuming write perms...

    def __init__ (self) :
        suggestify.Request.__init__(self, 'write')
    
    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return
        
        crumb = self.generate_crumb(self.user, 'method=unblock')
        self.assign('unblock_crumb', crumb)

        # fix me: pagination
        
        res = Blocked.blocked_by_user(self.user.nsid)
        blocked = res.fetch(20)

        users = []
        
        for b in blocked :
            users.append(User.get_user_by_nsid(b.blocked_nsid))

        self.assign('blocked_users', users)
        self.assign('count_blocked', len(users))

        #
        
        self.display('blocked.html')
        
