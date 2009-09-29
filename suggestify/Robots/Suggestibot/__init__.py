import suggestify.Robots

class Request (suggestify.Robots.Request) :

    def __init__ (self) :
        suggestify.Robots.Request.__init__(self, 'write')
        
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
        
        req_args = ('photo_id', 'lat', 'lon', '_s')
        sig_args = ['photo_id', 'lat', 'lon']

        if not self.ensure_required_args(req_args) :
            self.error('missing_args')
            return

        if not self.ensure_robot_sig(sig_args, self.request.get('_s')) :
            self.error('invalid_sig')
            return    

        #
        # get the photo
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
        # ensure the photo is owned by the logged in user
        #
        
        if rsp['photo']['owner'] != self.user.nsid :
            self.error('invalid_owner')
            return

        #
        # build a mock suggestion here
        #
        
        suggestion = {}
        
        self.assign('count_pending', 1)
        self.assign('pending', (suggestion,))

        approve_crumb = self.generate_crumb(self.user, 'method=approve')
        reject_crumb = self.generate_crumb(self.user, 'method=reject')
        block_crumb = self.generate_crumb(self.user, 'method=block')
        
        self.assign('approve_crumb', approve_crumb)
        self.assign('reject_crumb', reject_crumb)
        self.assign('block_crumb', block_crumb)

        #
        # Uh...what actually gets called when the user clicks ok?
        #
        
        self.display('review.html')
        return
