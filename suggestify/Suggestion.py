from google.appengine.ext import db
from suggestify.Tables import dbSuggestion

def status_map (self) :

    return {
        '0' : 'undefined',
        '1' : 'pending',
        '2' : 'approved',
        '3' : 'rejected'
    }

def create (args) :

    status = 1	# use the map please...
    
    # is it safe to use the Pt type or is that a Google-ism

    woeid = 0

    if args['woeid'] != '' :
        woeid = int(args['woeid'])
        
    s = dbSuggestion()
    s.photo_id = long(args['photo_id'])
    s.owner_nsid = args['owner_id']
    s.latitude = float(args['latitude'])
    s.longitude = float(args['longitude'])
    s.accuracy = int(args['accuracy'])
    s.woeid = woeid
    s.suggestor_nsid = args['suggestor_id']
    s.suggestor_username = args['suggestor_name']
    s.status = status
    s.context = args['context']
    s.put()
    
    return s

def has_pending_suggestions (photo_id, suggestor_nsid=None) :

    query_args = [ photo_id ]
    
    gql = "SELECT * FROM dbSuggestion WHERE photo_id = :1"

    if suggestor_nsid :

        query_args.append(suggestor_nsid)
        gql += " AND suggestor_nsid = :2"
        
    gql += " AND status=1"

    res = db.GqlQuery(gql, *query_args)
    return res.count()
    
def reject_all_pending_suggestions_for_owner (owner_nsid, suggestor_nsid=None) :

    query_args = [ owner_nsid ]
    
    gql = "SELECT * FROM dbSuggestion WHERE owner_nsid = :1"
    
    if suggestor_nsid :
        gql += " AND suggestor_nsid = :2"
        query_args.append( suggestor_nsid )

    gql += " AND status=1"
    
    pending = db.GqlQuery(gql, *query_args)

    for p in pending.fetch(pending.count()) :
        reject_suggestion(p)      

def reject_all_pending_suggestions_for_photo (photo_id) :

    gql = "SELECT * FROM dbSuggestion WHERE photo_id = :1 AND status=1"
    pending = db.GqlQuery(gql, photo_id)
    
    for p in pending.fetch(pending.count()) :
        reject_suggestion(p)

def reject_suggestion (suggestion) :
    suggestion.status = 3
    suggestion.put()

def approve_suggestion (suggestion) :
    suggestion.status = 2
    suggestion.put()
    
def fetch_pending_suggestion (suggestion_id) :

    gql = "SELECT * FROM dbSuggestion WHERE __key__ = :1"
    res = db.GqlQuery(gql, db.Key(suggestion_id))
    
    return res.get()
    
def pending_suggestions_for_user (nsid, photo_id=None) :

    query_args = [nsid]
    
    gql = "SELECT * FROM dbSuggestion WHERE owner_nsid = :1 AND status = 1"

    if photo_id :
        gql += " AND photo_id = :2"
        query_args.append(long(photo_id))
    
    pending = db.GqlQuery(gql, *query_args)
    return pending
