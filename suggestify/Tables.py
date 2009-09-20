from google.appengine.ext import db

class dbGamesRandom (db.Model) :

  suggestor_nsid = db.StringProperty()
  photo_id = db.IntegerProperty()
  
class dbSettings (db.Model) :

  nsid = db.StringProperty()
  email_address = db.StringProperty()
  email_address_pending = db.StringProperty()
  email_notifications = db.BooleanProperty()
  email_confirmation_code = db.StringProperty()
  comment_notifications = db.BooleanProperty()
  
class dbSuggestion (db.Model) :

  photo_id = db.IntegerProperty()
  owner_nsid = db.StringProperty()
  suggestor_nsid = db.StringProperty()
  suggestor_username = db.StringProperty()  
  latitude = db.FloatProperty()
  longitude = db.FloatProperty()  
  accuracy = db.IntegerProperty()
  woeid = db.IntegerProperty()
  context = db.IntegerProperty()
  created = db.DateTimeProperty(auto_now_add=True)  
  updated = db.DateTimeProperty(auto_now=True)
  status = db.IntegerProperty()
  comment_id = db.StringProperty()
