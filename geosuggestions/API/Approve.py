import geosuggestions.Suggestion as dbSuggestion
from geosuggestions.API.Core import CoreHandler

import FlickrApp.User as User

class ApproveHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb', 'suggestion_id', 'geo_perms', 'geo_context')
        
        if not ctx.ensure_args(required) :
            return 

        if not ctx.ensure_crumb('method=approve') :
            return

        suggestion_id = ctx.request.get('suggestion_id')
        suggestion = ctx.fetch_pending_suggestion(suggestion_id)
        
        if not suggestion:
            return 
    
        #
        # Check to see if the photo has already been geotagged
        #
    
        args = {
            'photo_id' : suggestion.photo_id,
            'auth_token' : ctx.user.token,
            'check_response' : 1,
            }

        """
        rsp = ctx.api_call('flickr.photos.getInfo', args)
        
        if not rsp :
            ctx.api_error(8, 'Unable to retrieve photo information from Flickr')
            return

        if rsp['photo'].has_key('location') :
            dbSuggestion.reject_all_pending_suggestions_for_photo(suggestion.photo_id)
        
            ctx.api_error(9, 'Photo has already been geotagged')
            return
        """
        
        #
        # Okay! Geotag the fucking photo!!!
        #

        accuracy = suggestion.accuracy

        if accuracy > 16 :
            accuracy = 16
            
        args = {'photo_id' : suggestion.photo_id,
                'lat' : suggestion.latitude,
                'lon' : suggestion.longitude,
                'accuracy' : accuracy,
                'auth_token' : ctx.user.token,
                }

        geo_context = ctx.request.get('geo_context')
        
        if geo_context and int(geo_context) != 0 :
            args['context'] = geo_context
            
        rsp = ctx.api_call('flickr.photos.geo.setLocation', args)
    
        if rsp['stat'] != 'ok' :
            ctx.api_error(10, 'Failed to set location: %s (%s)' % (rsp['message'], rsp['code']))
            return

        #
        # Geo perms
        #

        geoperms = int(ctx.request.get('geo_perms'))
        default = ctx.default_geoperms()

        if geoperms != default :

            method = 'flickr.photos.geo.setPerms'

            args = {
                'photo_id' : suggestion.photo_id,
                'auth_token' : ctx.user.token,
                'is_public' : 0,
                'is_contact' : 0,
                'is_family' : 0,
                'is_friend' : 0
            }
            
            if geoperms == 1 :
                args['is_public'] = 1
            elif geoperms == 2 :
                args['is_contact'] = 1
            elif geoperms == 3 :
                args['is_friend'] = 1
                args['is_family'] = 1
            elif geoperms == 4 :
                args['is_friend'] = 1                                
            elif geoperms == 5 :
                args['is_family'] = 1                
            else :
                pass

            rsp = ctx.api_call('flickr.photos.geo.setPerms', args)
    
            if rsp['stat'] != 'ok' :
                pass

            	# what then...
                # ctx.api_error(10, 'Failed to set location: %s (%s)' % (rsp['message'], rsp['code']))
                # return

        #
        # geo:suggestedby= machine tag but only if the geo perms are public
        #
        
        suggestor = User.get_user_by_nsid(suggestion.suggestor_nsid)

        if suggestor and geoperms == 1 :
            
            suggested_by = suggestor.nsid
            
            if suggestor.path_alias :
                suggested_by = suggestor.path_alias
                    
                tags = "geo:suggestedby=%s" % suggested_by
        
                args = {
                    'photo_id' : suggestion.photo_id,
                    'tags' : tags,
                    'auth_token' : ctx.user.token,
                    'check_response' : 1,
                }
        
                rsp = ctx.api_call('flickr.photos.addTags', args)

        #
        # update
        #
        
        dbSuggestion.approve_suggestion(suggestion)
            
        dbSuggestion.reject_all_pending_suggestions_for_photo(suggestion.photo_id)
        
        #
        # HAPPY
        #

        photo_owner = ctx.user.nsid

        if ctx.user.path_alias :
            photo_owner = ctx.user.path_alias
            
        photo_url = "http://www.flickr.com/photos/%s/%s" % (photo_owner, suggestion.photo_id)
        
        return ctx.api_ok({'photo_url' : photo_url})
