import suggestify.Robots
import FlickrApp.User as User

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

        if not self.validate_crumb(self.user, path, self.request.get('crumb')) :
            self.error('invalid_perms', is_api)
            return False

        #
        # args/sig validation
        #

        req_args = ('photo_id', 'lat', 'lon', 'acc', 'context', '_s')
        sig_args = ['photo_id', 'lat', 'lon', 'acc', 'context', 'woeid', 'crumb']

        if not self.ensure_required_args(req_args) :
            self.error('missing_args', is_api)
            return

        if not self.ensure_valid_args(req_args) :
            self.error('invalid_args', is_api)
            return

        if not self.ensure_robot_sig(sig_args, self.request.get('_s')) :
            self.error('invalid_sig')
            return    

        mock = self.generate_mock_suggestion()

        if not mock :
            return
        
        mock.status = 2
        suggestion = Suggestion.create(mock)

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
        reject_crumb = self.generate_crumb(self.user, 'method=reject')
        block_crumb = self.generate_crumb(self.user, 'method=block')
        
        self.assign('approve_crumb', approve_crumb)
        self.assign('reject_crumb', reject_crumb)
        self.assign('block_crumb', block_crumb)

        # TODO: generate a new sig with the crumb
        
	# TODO: assign suggested location params and sig here...
        
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
            'owner_nsid' : self.user.nsid,
            'suggestor_nsid' : suggestor.nsid,
            'suggestor_username' : suggestor.username,
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
