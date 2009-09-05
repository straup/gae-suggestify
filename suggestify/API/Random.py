from geosuggestions.API.Core import CoreHandler
from geosuggestions.Tables import dbGamesRandom

class NoIdeaHandler (CoreHandler) :

    def run (self, ctx) :

        required = ('crumb', 'photo_id')
        
        if not ctx.ensure_args(required) :
            return 

        if not ctx.ensure_crumb('method=noidea') :
            return

        # FIX ME: please to put me in a proper class...
        
        no = dbGamesRandom()
        no.photo_id = long(ctx.request.get('photo_id'))
        no.suggestor_nsid = ctx.user.nsid
        no.put()
        
        ctx.api_ok()
        
