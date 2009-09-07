import suggestify.API

class EchoHandler (suggestify.API.Request) :

    def run (self) :

        params = { 'param' : [] }
        
        for arg in self.request.arguments() :
            params['param'].append({arg : self.request.get(arg)})
            
        self.api_ok({'params' : params} )
        return

