from geosuggestions.API.Core import CoreHandler
import geosuggestions.Suggestion as Suggestion

class RejectHandler (CoreHandler) :

    def run (self, ctx) :
        required = ('crumb', 'suggestion_id')

        if not ctx.ensure_args(required) :
            return 

        if not ctx.ensure_crumb('method=reject') :
            return

        suggestion_id = ctx.request.get('suggestion_id')
        suggestion = ctx.fetch_pending_suggestion(suggestion_id)
        
        if not suggestion:
            return 

        Suggestion.reject_suggestion(suggestion)
        return ctx.api_ok()
