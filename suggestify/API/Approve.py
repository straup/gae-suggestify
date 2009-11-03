import suggestify.API
import suggestify.Suggestion as Suggestion

import FlickrApp.User as User
import config
import logging

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

        # Here's a potential problem: In order to do this properly
        # we may need to call the Flickr API (6) times and we're
        # doing all of them synchronously there's always the risk
        # that one of them will time out. Some possibilities include
        # doing the machinetag and comment stuff as queued tasks but
        # that probably puts too many eggs in the app engine basket.
        
        # Required:
        # flickr.photos.getInfo
        # flickr.photos.geo.setLocation

        # Possible:
        # flickr.photos.geo.setPerms        
        # flickr.photos.addTags
        # flickr.photos.comments.addComment
        
        #
        # Check to see if the photo has already been geotagged
        #
        
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

        #
        # Also, this is all cloned in Robots/Suggestibot <-- it should probably
        # go in a "library" but the whole thing gets wrapped up in boring
        # object/globals/self nonsense and the fact that there aren't any
        # in Suggestion.py
        #
        
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
        # geo:suggestedby= machine tag and comment-y reward
        # comment but only if the geo perms are public
        #

        if geoperms == 1 and suggestion.suggestor_nsid != self.user.nsid :

            suggested_by = suggestion.suggestor_nsid
            suggestor = User.get_user_by_nsid(suggestion.suggestor_nsid)
                    
            if suggestor and suggestor.path_alias :
                suggested_by = suggestor.path_alias

            tags = "geo:suggestedby=%s" % suggested_by
        
            machinetags_args = {
                'photo_id' : suggestion.photo_id,
                'tags' : tags,
                'auth_token' : self.user.token,
                'check_response' : 1,
                }

            rsp = self.api_call('flickr.photos.addTags', machinetags_args)

            # sudo make me a preference

            # TO DO: this should not be called "rewards" but it's early
            # and I haven't had much coffee....
            
            if self.user.nsid in config.rewards :

                suggested_date = suggestion.created.strftime("%B %d, %Y")
                suggestor_name = suggestor.username
                suggestor_url = 'http://www.flickr.com/photos/%s' % suggestor.nsid

                if suggestor.path_alias != '' :
                    suggestor_url = 'http://www.flickr.com/photos/%s' % suggestor.path_alias
                    
                # Note: don't lookup/display the place name for the WOE ID
                # until it's possible to do corrections on approval.

                nearby_url = "http://www.flickr.com/photos/%s/%s/nearby/?by=everyone&taken=recent&sort=distance&page=1&show=detail" % (self.user.nsid, suggestion.photo_id)
                
                comment = """On %s, <a href="%s">%s</a> suggested <a href="%s">where this photo was taken</a>, and they were right!
                """ % (suggested_date, suggestor_url, suggestor_name, nearby_url)

                method = 'flickr.photos.comments.addComment'
            
                comments_args = {
                    'photo_id' : suggestion.photo_id,
                    'comment_text' : comment,
                    'auth_token' : self.user.token,
                }
                
                rsp = self.api_call(method, comments_args)

                if not rsp :
                    logging.error("Failed to post approval comment")

                # TODO, MAYBE: delete initial suggestion comment here?
                
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

        #
        
        out = {'photo_url' : photo_url}            
        return self.api_ok(out)
