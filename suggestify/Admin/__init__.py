import suggestify
from google.appengine.ext import db

class Request (suggestify.Request) :

    def __init (self) :
        suggestify.Request.__init__(self)

class IndexHandler (Request) :

    def get (self) :

        self.response.out.write("[you are here]")
        return
