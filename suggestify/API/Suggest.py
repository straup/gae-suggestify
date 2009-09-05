from geosuggestions.API.Core import CoreHandler
import geosuggestions.Suggestion as Suggestion
import geosuggestions.Settings as Settings
import geosuggestions.Email as Email

import FlickrApp.User.Blocked as Blocked
import FlickrApp.User.Membership as Membership

class SuggestHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb', 'photo_id', 'owner_id', 'latitude', 'longitude')

        if not ctx.ensure_args(required) :
            return 

        #
        # Context
        #

        geo_context = ctx.request.get('geo_context')

        if geo_context :

            geo_context = int(geo_context)
            
            if not geo_context in (0, 1, 2) :
                ctx.api_error(3, 'Not a valid geo context')
                return
        else :

            geo_context = 0

        #
        #
        #
        
        if not ctx.ensure_crumb('method=suggest') :
            return

        owner_nsid = ctx.request.get('owner_id')
        photo_id = long(ctx.request.get('photo_id'))
        
        #
        # Blocked?
        #
    
        if Blocked.is_user_blocked(ctx.user.nsid, owner_nsid) :
            ctx.api_error(3, 'You do not have permission to suggest a location for this photo.')
            return

        #
        # Opted out
        #
        
        if Membership.has_user_opted_out(owner_nsid) :
            ctx.api_error(4, 'You do not have permission to suggest a location for this photo.')
            return
        
        #
        # Already suggested?
        # This query will probably need to be less blunt
        #

        if Suggestion.has_pending_suggestions(photo_id, ctx.user.nsid) :
            ctx.api_error(999, 'Already suggested')
            return

        #
        # grab the photo
        #

        method = 'flickr.photos.getInfo'
        
        args = {
            'photo_id' : photo_id,
        }
        
        rsp = ctx.proxy_api_call(method, args)
        
        #
        # Recordify!
        #
        
        owner_nsid = ctx.request.get('owner_id')
        
        args = {
            'photo_id' : photo_id,
            'owner_id' : owner_nsid,
            'latitude' : ctx.request.get('latitude'),
            'longitude' : ctx.request.get('longitude'),
            'accuracy' : ctx.request.get('accuracy'),
            'woeid' : ctx.request.get('woeid'),
            'suggestor_id' : ctx.user.nsid,
            'suggestor_name' : ctx.user.username,
            'context' : geo_context,
        }

        s = Suggestion.create(args)
        
        if not s :
            ctx.api_error(2, 'There was a problem recording your suggestion.')
            return

        #
        # Notifications?
        #

        settings = Settings.get_settings_for_user(owner_nsid)

        if settings and settings.email_notifications :

            review_link = "%s/review/%s" % (ctx.request.host_url, photo_id)
            
            to_addr = settings.email_address
            subject = 'You have a new suggestion for one of your photos!'
            body = """Greetings from the Suggestify project!

Flickr user %s has suggested a location for your photo %s!

To approve or reject this suggestion, follow the link below:

%s

(If you're tired of getting these email messages you can always disable email
notifications by going to: %s/settings/notifications)

Cheers,
            """ % (ctx.user.username, rsp['photo']['title']['_content'], review_link, ctx.request.host_url)

            Email.send(to=to_addr, subject=subject, body=body)
                
        #
        # OKAY!
        #
        
        ctx.api_ok()
        return
        
