from google.appengine.ext import db
from geosuggestions import Geosuggestions
from geosuggestions.Tables import dbSettings

def get_settings_for_user (nsid, auto_create=True) :

        gql = "SELECT * FROM dbSettings WHERE nsid = :1"
        res = db.GqlQuery(gql, nsid)
        settings = res.get()

        if settings :
            return settings

        if auto_create :
            return create_settings_for_user(nsid)

        return False
    
def create_settings_for_user (nsid) :

    settings = dbSettings()
    settings.nsid = nsid
    settings.email_notifications = False
    settings.email_confirmed = False            
    settings.comment_notifications = False            
    settings.put()
    
    return settings
            
class SettingsHandler (Geosuggestions) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return
        
        self.display("settings.html")
        return

class NotificationsHandler (Geosuggestions) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return

        settings = get_settings_for_user(self.user.nsid)
        self.assign("settings", settings)

        email_enable_crumb = self.generate_crumb(self.user, "method=enable_email")
        self.assign("email_enable_crumb", email_enable_crumb)
        
        if settings.email_notifications :
                email_disable_crumb = self.generate_crumb(self.user, "method=disable_email")
                self.assign("email_disable_crumb", email_disable_crumb)

        self.display("notifications.html")
        return

class EmailNotificationsConfirmHandler (Geosuggestions) :

    def get (self, code) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return
        
        settings = get_settings_for_user(self.user.nsid)
        confirmed = False
        
        if settings.email_confirmation_code == code :
            settings.email_address = settings.email_address_pending                
            settings.email_notifications = True
            settings.put()
            
            confirmed = True

        # Set to zero, no matter what
        
        settings.email_confirmation_code = ''
        settings.email_address_pending = ''
        settings.put()

        self.assign("type", "email")
        self.assign("confirmed", confirmed)
        
        self.display("confirmation.html")
        return
