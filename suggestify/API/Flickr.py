import suggestify.API

class PlacesGetInfoHandler (suggestify.API.Request) :

    def run (self) :

        required = ('woe_id',)

        if not self.ensure_args(required) :
            return 

        args = {
            'woe_id' : self.request.get('woe_id'),
            'auth_token' : self.user.token,
        }

        ttl = 60 * 60 * 14
        
        rsp = self.proxy_api_call('flickr.places.getInfo', args, ttl)

        # wrong and dirty, please to fix
        self.format = 'json'

        if not rsp :
            self.api_error(1, 'API call failed to anything')
            return
        
        if rsp['stat'] != 'ok' :
            self.api_error(2, 'API call failed: %s' % rsp['message'])
            return

        self.api_ok({'place' : rsp['place']})
        return

class PlacesReverseGeoHandler (suggestify.API.Request) :

    def run (self) :

        required = ('lat', 'lon', 'accuracy')

        if not self.ensure_args(required) :
            return 

        args = {
            'lat' : self.request.get('lat'),
            'lon' : self.request.get('lon'),
            'accuracy' : self.request.get('accuracy'),            
        }

        ttl = 60 * 60 * 14
        
        rsp = self.proxy_api_call('flickr.places.findByLatLon', args, ttl)

        # wrong and dirty, please to fix
        self.format = 'json'

        if not rsp :
            self.api_error(1, 'API call failed to anything')
            return
        
        if rsp['stat'] != 'ok' :
            self.api_error(2, 'API call failed: %s' % rsp['message'])
            return

        self.api_ok({'places' : rsp['places']})
        return
    
class FindByUsernameHandler (suggestify.API.Request) :

    def run (self) :

        required = ('username',)

        if not self.ensure_args(required) :
            return 

        args = {
            'username' : self.request.get('username'),
            'auth_token' : self.user.token,
        }

        ttl = 60 * 60 * 14
        
        rsp = self.proxy_api_call('flickr.people.findByUsername', args, ttl)

        # wrong and dirty, please to fix
        self.format = 'json'

        if not rsp :
            self.api_error(1, 'API call failed to anything')
            return
        
        if rsp['stat'] != 'ok' :
            self.api_error(2, 'API call failed: %s' % rsp['message'])
            return

        self.api_ok({'user' : rsp['user']})
        return
        
class PhotoGetInfoHandler (suggestify.API.Request) :

    def run (self) :

        required = ('photo_id', )

        if not self.ensure_args(required) :
            return 

        args = {
            'photo_id' : self.request.get('photo_id')
        }

        ttl = 60 * 60
        
        rsp = self.proxy_api_call('flickr.photos.getInfo', args, ttl)

        # wrong and dirty, please to fix
        self.format = 'json'

        if not rsp :
            self.api_error(1, 'API call failed to anything')
            return
        
        if rsp['stat'] != 'ok' :
            self.api_error(2, 'API call failed: %s' % rsp['message'])
            return

        self.api_ok({'photo' : rsp['photo']})
        return

    
class PeopleGetInfoHandler (suggestify.API.Request) :

    def run (self) :

        required = ('user_id', )

        if not self.ensure_args(required) :
            return 

        args = {
            'user_id' : self.request.get('user_id')
        }

        ttl = 60 * 60 * 7
        
        rsp = self.proxy_api_call('flickr.people.getInfo', args, ttl)

        # wrong and dirty, please to fix
        self.format = 'json'
        
        if rsp['stat'] != 'ok' :
            self.api_error(1, 'API call failed to return anything')
            return

        if not rsp :
            self.api_error(2, 'API call failed: %s' % rsp['message'])
            return

        self.api_ok({'person' : rsp['person']})
        return
