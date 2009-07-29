from geosuggestions.API.Core import CoreHandler
import geosuggestions.Suggestion as dbSuggestion
import FlickrApp.User.Blocked as Blocked

class BlockHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb', 'user_id')

        if not ctx.ensure_args(required) :
            return 

        if not ctx.ensure_crumb('method=block') :
            return

        blocked_nsid = ctx.request.get('user_id')
        blocker_nsid = ctx.user.nsid
        
        # This will probably change
        
        Blocked.block_user(blocked_nsid, blocker_nsid)

        dbSuggestion.reject_all_pending_suggestions_for_owner(blocker_nsid, blocked_nsid)
        
        ctx.api_ok()
        return

class UnBlockHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb', 'user_id')

        if not ctx.ensure_args(required) :
            return 

        if not ctx.ensure_crumb('method=unblock') :
            return

        blocked_nsid = ctx.request.get('user_id')

        # This will probably change
        
        Blocked.unblock_user(blocked_nsid, ctx.user.nsid)

        ctx.api_ok()
        return
