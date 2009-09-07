import suggestify.API
import suggestify.Suggestion as Suggestion

import FlickrApp.User as User

class ApproveHandler (suggestify.API.Request) :

    def run (self) :

        required = ('crumb', 'suggestion_id', 'geo_perms', 'geo_context')
        
        if not self.ensure_args(required) :
            return 

        if not self.ensure_crumb('method=approve') :
            return

        suggestion_id = self.request.get('suggestion_id')
        suggestion = self.fetch_pending_suggestion(suggestion_id)
        
        if not suggestion:
            return 
    
        #
        # Check to see if the photo has already been geotagged
        #

	# Note: It's no longer clear why this got commented out.
        # My guess is because it was I was concerend about the
        # actual approval timing out. There are two things to
        # consider here: 1) scrumjax-ing the check when a user
        # hits approve 2) storing a local index of photos that
        # have been geotgged either by suggestify or during a
        # separate check 3) all of the above.
        #
        # (20090905/asc)
        
        """
        
        args = {
            'photo_id' : suggestion.photo_id,
            'auth_token' : self.user.token,
            'check_response' : 1,
            }

        rsp = self.api_call('flickr.photos.getInfo', args)
        
        if not rsp :
            self.api_error(8, 'Unable to retrieve photo information from Flickr')
            return

        if rsp['photo'].has_key('location') :
            Suggestion.reject_all_pending_suggestions_for_photo(suggestion.photo_id)
        
            self.api_error(9, 'Photo has already been geotagged')
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
                'auth_token' : self.user.token,
                }

        geo_context = self.request.get('geo_context')
        
        if geo_context and int(geo_context) != 0 :
            args['context'] = geo_context
            
        rsp = self.api_call('flickr.photos.geo.setLocation', args)

        if not rsp :
            self.api_error(10, 'Failed to set location: Flickr API call failed')
            
        if rsp['stat'] != 'ok' :
            self.api_error(10, 'Failed to set location: %s (%s)' % (rsp['message'], rsp['code']))
            return

        #
        # Geo perms (it would be better if you could assign perms in setLocation...)
        #

        geoperms = int(self.request.get('geo_perms'))
        default = self.default_geoperms()

        if geoperms != default :

            method = 'flickr.photos.geo.setPerms'

            args = {
                'photo_id' : suggestion.photo_id,
                'auth_token' : self.user.token,
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

            rsp = self.api_call('flickr.photos.geo.setPerms', args)
    
            if rsp['stat'] != 'ok' :
                msg = 'Failed to set location: %s (%s)' % (rsp['message'], rsp['code'])
                self.log(msg, 'warning')
                pass

        #
        # geo:suggestedby= machine tag but only if the geo perms are public
        #

	# This is probably a good candidate to do client-side if the approval
        # returns OK
        
        if geoperms == 1 and suggestion.suggestor_nsid != self.user.nsid :

            # NSID is the default
            
            suggested_by = suggestion.suggestor_nsid

            # But try to get their path alias (since this is immutable)
            
            suggestor = User.get_user_by_nsid(suggestion.suggestor_nsid)
                    
            if suggestor and suggestor.path_alias :
                suggested_by = suggestor.path_alias

            # Now tag
            
            tags = "geo:suggestedby=%s" % suggested_by
        
            args = {
                'photo_id' : suggestion.photo_id,
                'tags' : tags,
                'auth_token' : self.user.token,
                'check_response' : 1,
                }
        
            rsp = self.api_call('flickr.photos.addTags', args)

        #
        # Update (possibly do this before setting tags?)
        #
        
        Suggestion.approve_suggestion(suggestion)
        Suggestion.reject_all_pending_suggestions_for_photo(suggestion.photo_id)
        
        #
        # HAPPY
        #

        photo_owner = self.user.nsid

        if self.user.path_alias :
            photo_owner = self.user.path_alias
            
        photo_url = "http://www.flickr.com/photos/%s/%s" % (photo_owner, suggestion.photo_id)
        
        return self.api_ok({'photo_url' : photo_url})
