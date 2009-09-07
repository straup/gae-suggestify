import suggestify

class PrefsHandler (suggestify.Request) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return
        
        self.display("settings.html")
        return

class NotificationsHandler (suggestify.Request) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return

        self.assign("settings", self.user.settings)

        email_enable_crumb = self.generate_crumb(self.user, "method=enable_email")
        self.assign("email_enable_crumb", email_enable_crumb)
        
        if self.user.settings.email_notifications :
                email_disable_crumb = self.generate_crumb(self.user, "method=disable_email")
                self.assign("email_disable_crumb", email_disable_crumb)

        self.display("notifications.html")
        return

class EmailNotificationsConfirmHandler (suggestify.Request) :

    def get (self, code) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return
        
        confirmed = False
        
        if self.user.settings.email_confirmation_code == code :
            self.user.settings.email_address = settings.email_address_pending                
            self.user.settings.email_notifications = True
            self.user.settings.put()
            
            confirmed = True

        # Set to zero, no matter what
        
        self.user.settings.email_confirmation_code = ''
        self.user.settings.email_address_pending = ''
        self.user.settings.put()

        self.assign("type", "email")
        self.assign("confirmed", confirmed)
        
        self.display("confirmation.html")
        return

