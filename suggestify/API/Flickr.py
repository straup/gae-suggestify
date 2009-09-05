from geosuggestions.API.Core import CoreHandler

class PlacesGetInfoHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('woe_id',)

        if not ctx.ensure_args(required) :
            return 

        args = {
            'woe_id' : ctx.request.get('woe_id'),
            'auth_token' : ctx.user.token,
        }

        ttl = 60 * 60 * 14
        
        rsp = ctx.proxy_api_call('flickr.places.getInfo', args, ttl)

        # wrong and dirty, please to fix
        ctx.format = 'json'
        
        if rsp['stat'] != 'ok' :
            ctx.api_error(1, 'API call failed')
            return

        ctx.api_ok({'place' : rsp['place']})
        return
    
class FindByUsernameHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('username',)

        if not ctx.ensure_args(required) :
            return 

        args = {
            'username' : ctx.request.get('username'),
            'auth_token' : ctx.user.token,
        }

        ttl = 60 * 60 * 14
        
        rsp = ctx.proxy_api_call('flickr.people.findByUsername', args, ttl)

        # wrong and dirty, please to fix
        ctx.format = 'json'
        
        if rsp['stat'] != 'ok' :
            ctx.api_error(1, 'API call failed')
            return

        ctx.api_ok({'user' : rsp['user']})
        return
        
class PhotoGetInfoHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('photo_id', )

        if not ctx.ensure_args(required) :
            return 

        args = {
            'photo_id' : ctx.request.get('photo_id')
        }

        ttl = 60 * 60
        
        rsp = ctx.proxy_api_call('flickr.photos.getInfo', args, ttl)

        # wrong and dirty, please to fix
        ctx.format = 'json'
        
        if rsp['stat'] != 'ok' :
            ctx.api_error(1, 'API call failed')
            return

        ctx.api_ok({'photo' : rsp['photo']})
        return

    
class PeopleGetInfoHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('user_id', )

        if not ctx.ensure_args(required) :
            return 

        args = {
            'user_id' : ctx.request.get('user_id')
        }

        ttl = 60 * 60 * 7
        
        rsp = ctx.proxy_api_call('flickr.people.getInfo', args, ttl)

        # wrong and dirty, please to fix
        ctx.format = 'json'
        
        if rsp['stat'] != 'ok' :
            ctx.api_error(1, 'API call failed')
            return

        ctx.api_ok({'person' : rsp['person']})
        return

