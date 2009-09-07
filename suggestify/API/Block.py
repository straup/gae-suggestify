import suggestify
import suggestify.Suggestion as Suggestion
import FlickrApp.User.Blocked as Blocked

class BlockHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb', 'user_id')

        if not self.ensure_args(required) :
            return 

        if not self.ensure_crumb('method=block') :
            return

        blocked_nsid = self.request.get('user_id')
        blocker_nsid = self.user.nsid
        
        # This will probably change
        
        Blocked.block_user(blocked_nsid, blocker_nsid)

        Suggestion.reject_all_pending_suggestions_for_owner(blocker_nsid, blocked_nsid)
        
        self.api_ok()
        return

class UnBlockHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb', 'user_id')

        if not self.ensure_args(required) :
            return 

        if not self.ensure_crumb('method=unblock') :
            return

        blocked_nsid = self.request.get('user_id')

        # This will probably change
        
        Blocked.unblock_user(blocked_nsid, self.user.nsid)

        self.api_ok()
        return
