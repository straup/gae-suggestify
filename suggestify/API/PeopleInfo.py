# please to use wrapper/helper functions in FlickrApp

import suggestify.API
import FlickrApp.User as User

import os.path

class PeopleInfo (suggestify.API.Request) :

    def __init__ (self) :
        suggestify.API.Request.__init__(self)
        self.info = {}

    def get_people_info (self, ctx, nsid) :

        if not self.info.has_key(nsid) :

            method = 'flickr.people.getInfo'
            args = { 'user_id' : nsid, 'check_response' : 1 }

            rsp = ctx.api_call(method, args);
            self.info[nsid] = rsp
            
        return self.info[nsid]

class PathAliasHandler (PeopleInfo) :

    def run (self) :

        required = ('user_id',)

        if not self.ensure_args(required) :
            return 

	user_id = self.request.get('user_id')
        
        user = User.get_user_by_nsid(user_id)
        
        if not user :
            self.api_error(1, 'Not a valid user')
            return

        if user.path_alias :
            self.api_ok({'buddyicon_url' : user.buddyicon_url})
            return

        rsp = self.get_people_info(self, user.nsid)

        if not rsp :
            self.api_error(2, 'Failed to retrieve buddyicon')
            return

        url = rsp['person']['photosurl']['_content']

        if url.endswith("/") :
            url = url[:-1]

        path_alias = os.path.basename(url)

        if path_alias == user.nsid :
            self.api_error(1, 'No path alias defined')

        User.set_path_alias(user, path_alias)

        self.api_ok({'path_alias' : path_alias})
        return
    
class BuddyiconHandler (PeopleInfo) :
        
    def run (self) :

        required = ('user_id',)

        if not self.ensure_args(required) :
            return 

	user_id = self.request.get('user_id')
        
        user = User.get_user_by_nsid(user_id)
        
        if not user :
            self.api_error(1, 'Not a valid user')
            return

        if user.buddyicon_url :
            self.api_ok({'buddyicon_url' : user.buddyicon_url})
            return

        rsp = self.get_people_info(self, user.nsid)

        if not rsp :
            self.api_error(2, 'Failed to retrieve buddyicon')
            return

        if rsp['person']['iconfarm'] == 0 :
            self.api_error(3, 'User has not chosen a buddyicon')
            return
        
        buddyicon = "http://farm%s.static.flickr.com/%s/buddyicons/%s.jpg" % (rsp['person']['iconfarm'], rsp['person']['iconserver'], self.user.nsid)

        User.set_buddyicon_url(user, buddyicon)

        self.api_ok({'buddyicon_url' : buddyicon})
        return
