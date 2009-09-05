from geosuggestions.API.Core import CoreHandler
import geosuggestions.Settings as Settings
import geosuggestions.Email as Email
            
class EmailEnableHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb', 'email')

        if not ctx.ensure_args(required) :
            return

        if not ctx.ensure_crumb('method=enable_email') :
            return

        email = ctx.request.get('email')
        
        if not Email.is_valid_address(email) :
            ctx.api_error(1, 'Invalid email address')
            return

        #
        
        settings = Settings.get_settings_for_user(ctx.user.nsid)

        if not settings :
            ctx.api_error(2, 'Unable to load user settings')
            return
        
        # la la la - I can't hear you.
        
        if email == settings.email_address :
            ctx.api_ok()
            return
        
        #

        confirmation_code = ctx.generate_confirmation_code(12)

        settings.email_address_pending = email
        settings.email_confirmation_code = confirmation_code
        settings.put()
        
        # 

        confirmation_url = "%s/confirm/e/%s" % (ctx.request.host_url, confirmation_code)
                
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
            ctx.api_error(3, 'There was a problem delivering email')
            return
        
        ctx.api_ok()
        return
    
class EmailDisableHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb',)

        if not ctx.ensure_args(required) :
            return

        if not ctx.ensure_crumb('method=disable_email') :
            return

        settings = Settings.get_settings_for_user(ctx.user.nsid)

        if not settings :
            ctx.api_error(1, 'Unable to load user settings')
            return

        settings.email_address = ''
        settings.email_notifications = False
        settings.put()

        ctx.api_ok()
        return
