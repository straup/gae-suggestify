import suggestify.API
import suggestify.Suggestion as Suggestion

class RejectHandler (suggestify.API.Request) :

    def run (self) :
        required = ('crumb', 'suggestion_id')

        if not self.ensure_args(required) :
            return 

        if not self.ensure_crumb('method=reject') :
            return

        suggestion_id = self.request.get('suggestion_id')
        suggestion = self.fetch_pending_suggestion(suggestion_id)
        
        if not suggestion:
            return 

        Suggestion.reject_suggestion(suggestion)
        return self.api_ok()
