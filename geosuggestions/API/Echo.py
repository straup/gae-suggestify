from geosuggestions.API.Core import CoreHandler

class EchoHandler (CoreHandler) :

    def run (self, ctx) :

        params = { 'param' : [] }
        
        for arg in ctx.request.arguments() :
            params['param'].append({arg : ctx.request.get(arg)})
            
        ctx.api_ok({'params' : params} )
        return

