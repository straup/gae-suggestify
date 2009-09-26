import suggestify
from google.appengine.ext import db

from FlickrApp.Tables import dbFlickrUser

import FlickrApp.User.Membership as Membership
import suggestify.Settings as Settings
import suggestify.Suggestion as Suggestion

import math

class Request (suggestify.Request) :

    def __init (self) :
        suggestify.Request.__init__(self)

class IndexHandler (Request) :

    def get (self) :

        self.response.out.write("[you are here]")
        return

class UsersHandler (Request) :

    def get (self, page=None) :

        if not page :
            page = 1

        page = int(page)
        per_page = 10

        offset = (page - 1) * per_page
        
        res = dbFlickrUser.all().order("-created")
        count = res.count()
        
        users = res.fetch(per_page, offset)

        perms = dict([(v, k) for (k, v) in self.perms_map.iteritems()])
        
        for u in users :
            u.settings = Settings.get_settings_for_user(u.nsid)
            u.opted_out = Membership.has_user_opted_out(u.nsid)

            u.created_ymd = u.created.date
            u.perms_str = perms[ u.perms ]
            
            u.count_suggested_for = Suggestion.count_suggestions_for_user(u.nsid)
            
            u.count_suggested_by = Suggestion.count_suggestions_by_user(u.nsid)
            u.count_suggested_by_approved = Suggestion.count_suggestions_by_user(u.nsid, 2)
            u.count_suggested_by_rejected = Suggestion.count_suggestions_by_user(u.nsid, 3)            
            
        pages = math.ceil(float(count) / float(per_page))
        
        if pages > page :
            self.assign("next", page + 1)

        if page > 1 : 
            self.assign("prev", page - 1)
        
        self.assign("count", count)
        self.assign("pages", pages)        
        self.assign("page", page)
        self.assign("per_page", per_page)
        self.assign("offset", offset)
        
        self.assign("users", users)
        self.display("admin_users.html")
        return
