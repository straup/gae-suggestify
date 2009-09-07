import suggestify.API
import suggestify.Settings as Settings
import suggestify.Email as Email

class EmailEnableHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb', 'email')

        if not self.ensure_args(required) :
            return

        if not self.ensure_crumb('method=enable_email') :
            return

        email = self.request.get('email')
        
        if not Email.is_valid_address(email) :
            self.api_error(1, 'Invalid email address')
            return

        #
        
        settings = Settings.get_settings_for_user(self.user.nsid)

        if not settings :
            self.api_error(2, 'Unable to load user settings')
            return
        
        # la la la - I can't hear you.
        
        if email == settings.email_address :
            self.api_ok()
            return
        
        #

        confirmation_code = self.generate_confirmation_code(12)

        settings.email_address_pending = email
        settings.email_confirmation_code = confirmation_code
        settings.put()
        
        # 

        confirmation_url = "%s/confirm/e/%s" % (self.request.host_url, confirmation_code)
                
        subject = "The Suggestify project would like you to confirm something"
        body = """Greetings from Suggestify project!
        
You've asked to be notified by email when someone adds a new suggestion
to one of your photos.

If you didn't ask for this, or simply don't remember asking, to be notified
the best thing to do is to ignore this email entirely. You can always ask
again when you're ready

Otherwise, click on the link below to finish setting up your email address
for notifications!

%s

Cheers,
        """ % confirmation_url

        if not Email.send(to=email, subject=subject, body=body) :
            self.api_error(3, 'There was a problem delivering email')
            return
        
        self.api_ok()
        return
    
class EmailDisableHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb',)

        if not self.ensure_args(required) :
            return

        if not self.ensure_crumb('method=disable_email') :
            return

        settings = Settings.get_settings_for_user(self.user.nsid)

        if not settings :
            self.api_error(1, 'Unable to load user settings')
            return

        settings.email_address = ''
        settings.email_notifications = False
        settings.put()

        self.api_ok()
        return
