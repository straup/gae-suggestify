import suggestify.API
import suggestify.Suggestion as Suggestion
import suggestify.Settings as Settings
import suggestify.Email as Email

import FlickrApp.User.Blocked as Blocked
import FlickrApp.User.Membership as Membership

class SuggestHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb', 'photo_id', 'owner_id', 'latitude', 'longitude')

        if not self.ensure_args(required) :
            return 

        #
        # Context
        #

        geo_context = self.request.get('geo_context')

        if geo_context :

            geo_context = int(geo_context)
            
            if not geo_context in (0, 1, 2) :
                self.api_error(3, 'Not a valid geo context')
                return
        else :

            geo_context = 0

        #
        #
        #
        
        if not self.ensure_crumb('method=suggest') :
            return

        owner_nsid = self.request.get('owner_id')
        photo_id = long(self.request.get('photo_id'))
        
        #
        # Blocked?
        #
    
        if Blocked.is_user_blocked(self.user.nsid, owner_nsid) :
            self.api_error(3, 'You do not have permission to suggest a location for this photo.')
            return

        #
        # Opted out
        #
        
        if Membership.has_user_opted_out(owner_nsid) :
            self.api_error(4, 'You do not have permission to suggest a location for this photo.')
            return
        
        #
        # Already suggested?
        # This query will probably need to be less blunt
        #

        if Suggestion.has_pending_suggestions(photo_id, self.user.nsid) :
            self.api_error(999, 'Already suggested')
            return

        #
        # grab the photo
        #

        method = 'flickr.photos.getInfo'
        
        args = {
            'photo_id' : photo_id,
        }
        
        rsp = self.proxy_api_call(method, args)
        
        #
        # Recordify!
        #
        
        owner_nsid = self.request.get('owner_id')
        
        args = {
            'photo_id' : photo_id,
            'owner_id' : owner_nsid,
            'latitude' : self.request.get('latitude'),
            'longitude' : self.request.get('longitude'),
            'accuracy' : self.request.get('accuracy'),
            'woeid' : self.request.get('woeid'),
            'suggestor_id' : self.user.nsid,
            'suggestor_name' : self.user.username,
            'context' : geo_context,
        }

        s = Suggestion.create(args)
        
        if not s :

            msg = "failed to add suggestion for %s" % str(args)
            self.log(msg, 'warning')
            
            self.api_error(2, 'There was a problem recording your suggestion.')
            return

        #
        # Notifications?
        #

        settings = Settings.get_settings_for_user(owner_nsid)

        if settings and settings.email_notifications :

            review_link = "%s/review/%s" % (self.request.host_url, photo_id)
            
            to_addr = settings.email_address
            subject = 'You have a new suggestion for one of your photos!'
            body = """Greetings from the Suggestify project!

Flickr user %s has suggested a location for your photo "%s".

To approve or reject this suggestion, follow the link below:

%s

(If you're tired of getting these email messages you can always disable email
notifications by going to: %s/settings/notifications)

Cheers,
            """ % (self.user.username, rsp['photo']['title']['_content'], review_link, self.request.host_url)

            Email.send(to=to_addr, subject=subject, body=body)
                
        #
        # OKAY!
        #
        
        self.api_ok()
        return
