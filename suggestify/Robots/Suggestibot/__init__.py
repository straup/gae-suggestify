import suggestify.Robots
import FlickrApp.User as User
import suggestify.Suggestion as Suggestion

import re

class Request (suggestify.Robots.Request) :

    def __init__ (self) :
        suggestify.Robots.Request.__init__(self, 'write')

    def ensure_valid_args (self, args) :

        coord = re.compile(r"^-?\d+(?:\.\d+)?$")
        photo = re.compile(r"^\d+$")
        
        for k in args :

            v = self.request.get(k)
      
            if k == 'photo_id' :

                if not photo.match(v) :
                    return False

            if k == 'lat' or k == 'lon' :

                if not coord.match(v) :
                    return False

            if k == 'acc' :

                if not int(v) in range(1, 17) :
                    return False
        
            if k == 'context' :

                if not int(v) in (0, 1, 2) :
                    return False

        return True

    def post (self, uuid) :

        is_api = True

        if not self.ensure_config(uuid) :
            self.error('invalid_config', is_api)
            return
        
        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return

        if not self.validate_crumb(self.user, 'method=approve', self.request.get('crumb')) :
            self.error('invalid_perms', is_api)
            return False

        #
        # args/sig validation
        #

        req_args = ('photo_id', 'lat', 'lon', 'acc', 'context', '_s')
        sig_args = ['photo_id', 'lat', 'lon', 'acc', 'context', 'woeid']

        if not self.ensure_required_args(req_args) :
            self.error('missing_args', is_api)
            return

        if not self.ensure_valid_args(req_args) :
            self.error('invalid_args', is_api)
            return

        if not self.ensure_robot_sig(sig_args, self.request.get('_s')) :
            self.error('invalid_sig')
            return    

        # TODO: woeid hoohah <-- should it be fetched again?
        
        # TODO: check for exisiting suggestion
        
        mock = self.generate_mock_suggestion()

        if not mock :
            return
        
        suggestion = Suggestion.create(mock)

        #
        # this is all copy/pasted out og API/Approve <-- it should probably go in a "library"
        #
                    
        args = {'photo_id' : suggestion.photo_id,
                'lat' : suggestion.latitude,
                'lon' : suggestion.longitude,
                'accuracy' : suggestion.accuracy,
                'auth_token' : self.user.token,
                }

        geo_context = self.request.get('geo_context')
        
        if geo_context and int(geo_context) != 0 :
            args['context'] = geo_context
            
        rsp = self.api_call('flickr.photos.geo.setLocation', args)

        if not rsp :
            self.error('Failed to set location: Flickr API call failed', is_api)
            return
        
        if rsp['stat'] != 'ok' :
            self.error('Failed to set location: %s (%s)' % (rsp['message'], rsp['code']), is_api)
            return

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
        
        if geoperms == 1 and suggestion.suggestor_nsid != self.user.nsid :

            suggested_by = suggestion.suggestor_nsid

            suggestor = User.get_user_by_nsid(suggestion.suggestor_nsid)
                    
            if suggestor and suggestor.path_alias :
                suggested_by = suggestor.path_alias
            
            tags = "geo:suggestedby=%s" % suggested_by
        
            args = {
                'photo_id' : suggestion.photo_id,
                'tags' : tags,
                'auth_token' : self.user.token,
                'check_response' : 1,
                }
        
            rsp = self.api_call('flickr.photos.addTags', args)
        
        Suggestion.approve_suggestion(suggestion)
        
        photo_owner = self.user.nsid

        if self.user.path_alias :
            photo_owner = self.user.path_alias
            
        photo_url = "http://www.flickr.com/photos/%s/%s" % (photo_owner, suggestion.photo_id)

        # END OF copy/paste code
        
        # TODO: return ok!
        
    def get (self, uuid) :

        #
        # who is on first?
        #
        
        if not self.ensure_config(uuid) :
            self.error('invalid_config')
            return
        
        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return

        #
        # args/sig validation
        #

        req_args = ('photo_id', 'lat', 'lon', 'acc', 'context', '_s')
        sig_args = ['photo_id', 'lat', 'lon', 'acc', 'context', 'woeid']

        if not self.ensure_required_args(req_args) :
            self.error('missing_args')
            return

        if not self.ensure_valid_args(req_args) :
            self.error('invalid_args')
            return

        if not self.ensure_robot_sig(sig_args, self.request.get('_s')) :
            self.error('invalid_sig')
            return    
        
        suggestion = self.generate_mock_suggestion()

        if not suggestion :
            return
        
        self.assign('count_pending', 1)
        self.assign('pending', (suggestion,))

        approve_crumb = self.generate_crumb(self.user, 'method=approve')
        block_crumb = self.generate_crumb(self.user, 'method=block')
        
        self.assign('approve_crumb', approve_crumb)
        self.assign('block_crumb', block_crumb)

        self.assign('robot_sig', self.request.get('_s'))
        self.assign('robot_photo_id', self.request.get('photo_id'))
        self.assign('robot_lat', self.request.get('lat'))
        self.assign('robot_lon', self.request.get('lon'))
        self.assign('robot_acc', self.request.get('acc'))
        self.assign('robot_context', self.request.get('context'))        
        self.assign('robot_uuid', uuid)

        geo_perms = self.default_geoperms()
        self.assign('geo_perms', geo_perms)
        
        self.display('suggestibot.html')
        return

    def generate_mock_suggestion (self) :

        #
        # Get the photo
        #

        method = 'flickr.photos.getInfo'
        photo_id = self.request.get('photo_id')        
        
        args = {
            'photo_id' : photo_id,
            'auth_token' : self.user.token,
            }
        
        rsp = self.proxy_api_call(method, args)

        if not rsp or rsp['stat'] != 'ok' :
            self.error('no_photoinfo')
            return

        #
        # Ensure the photo is owned by the logged in user
        #
        
        if rsp['photo']['owner']['nsid'] != self.user.nsid :
            self.error('invalid_owner')
            return

        #
        # Ensure the photo isn't already geotagged
        #

        if rsp['photo'].has_key('location') :
            self.error('already_geotagged')
            return
        
        #
	# Create a mock suggestion
        #
        
        suggestor = User.get_user_by_nsid(self.config['flickr_nsid'])

        woeid = 0

        if self.request.get('woeid') != '' :
            woeid = self.request.get('woeid')
            
        suggestion = {
            'photo_id' : int(photo_id),
            'owner_id' : self.user.nsid,
            'suggestor_id' : suggestor.nsid,
            'suggestor_name' : suggestor.username,
            'latitude' : float(self.request.get('lat')),
            'longitude' : float(self.request.get('lon')),
            'accuracy' : int(self.request.get('acc')),  
            'woeid' : woeid,
            'context' : int(self.request.get('context')),
            # 'created' : 'datetime'
            # 'updated' : 'datetime'
            'status' : 1,
            'comment_id' : '',
            }

        return suggestion
