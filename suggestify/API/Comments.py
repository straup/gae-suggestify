import suggestify.API
import suggestify.Settings as Settings

# Note to self: this is an awful lot of boiler
# plate for a basic get/set handler...

class CommentsEnableHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb',)

        if not self.ensure_args(required) :
            return

        if not self.ensure_crumb('method=enable_comments') :
            return

        #
        
        settings = Settings.get_settings_for_user(self.user.nsid)

        if not settings :
            self.api_error(2, 'Unable to load user settings')
            return
        
        settings.comment_notifications = True
        settings.put()

        self.api_ok()
        return
    
class CommentsDisableHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb',)

        if not self.ensure_args(required) :
            return

        if not self.ensure_crumb('method=disable_comments') :
            return

        #
        
        settings = Settings.get_settings_for_user(self.user.nsid)

        if not settings :
            self.api_error(2, 'Unable to load user settings')
            return
        
        settings.comment_notifications = False
        settings.put()

        self.api_ok()
        return
