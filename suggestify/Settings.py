from suggestify.Tables import dbSettings
from google.appengine.ext import db

def get_settings_for_user (nsid, auto_create=True) :

        gql = "SELECT * FROM dbSettings WHERE nsid = :1"
        res = db.GqlQuery(gql, nsid)
        settings = res.get()

        if settings :
            return settings

        if auto_create :
            return create_settings_for_user(nsid)

        return False
    
def create_settings_for_user (nsid) :

    settings = dbSettings()
    settings.nsid = nsid
    settings.email_notifications = False
    settings.email_confirmed = False            
    settings.comment_notifications = False            
    settings.put()
    
    return settings
