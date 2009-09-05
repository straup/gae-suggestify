from geosuggestions.API.Core import CoreHandler
import FlickrApp.User.Membership as Membership
import FlickrApp.User.Blocked as Blocked
from google.appengine.ext import db

import random
import time

class SearchRandomByContactsHandler (CoreHandler) :

    def run (self, ctx) :

        if ctx.request.get('page') != '' :
            page = ctx.request.get('page')

        page = 1

        if ctx.request.get('page') :
            page = ctx.request.get('page')
            
        per_page = max(int(random.random() * 100), 25)
    
        sort = ['date-posted-asc',
                'date-posted-desc',
                'date-taken-asc',
                'date-taken-desc',
                'interestingness-desc',
                'interestingness-asc',
                'relevance']
            
        random.shuffle(sort)
        random.shuffle(sort)
            
        contacts = ['ff', 'all']
        random.shuffle(contacts)

        prop = random.random()
        format = "%Y-%m-%d"
        stime = time.mktime(time.strptime('1970-01-01', format))
        etime = time.time()
        
        ptime = stime + prop * (etime - stime)
    
        date_taken  = time.strftime(format, time.localtime(ptime))

        method = 'flickr.photos.search'
        
        args = {
            'auth_token' : ctx.user.token,
            'user_id' : ctx.user.nsid,
            'contacts' : contacts[0],
            'has_geo' : 0,
            'per_page' : per_page,
            'page' : page,
            'sort' : sort[0],
            'max_taken_date' : "%s 00:00:00" % date_taken,
            'extras' : 'owner_name,date_taken,tags'
            }

        ttl = 60 * 10

        rsp = self.proxy_api_call(method, args, ttl)

        # wrong and dirty, please to fix
        ctx.format = 'json'
            
        if not rsp or rsp['stat'] != 'ok' :
            ctx.api_error(1, 'API call failed')
            return
        
        if rsp['photos']['total'] == 0 :
            ctx.api_error(2, 'Retry, no photos for query');
            return

        # these always time out on localhost...
        
        if ctx.request.host.startswith("localhost") :
            ctx.api_ok({'photos' : rsp['photos']})
            return
    
        skip_photos = []
        unknown_photos = []    
        filtered = []
        
        blocked_by = {}
        opted_out = {}

        # please to memcache all of this...
            
        gql = "SELECT * FROM dbSuggestion WHERE suggestor_nsid = :1"
        res = db.GqlQuery(gql, ctx.user.nsid)
        
        for ph in res.fetch(res.count()) :
            skip_photos.append(ph.photo_id)

        gql = "SELECT * FROM dbGamesRandom WHERE suggestor_nsid = :1"
        res = db.GqlQuery(gql, ctx.user.nsid)
    
        for ph in res.fetch(res.count()) :
            unknown_photos.append(ph.photo_id)
            
        for ph in rsp['photos']['photo'] :

            id = long(ph['id'])
            
            if id in skip_photos :
                continue

            if id in unknown_photos :
                continue

            # has the photo owner opted out

            photo_owner = ph['owner']
        
            if not opted_out.has_key(photo_owner) :
                has_opted_out = Membership.has_user_opted_out(photo_owner)
                opted_out[photo_owner] = has_opted_out

            if opted_out[photo_owner] :
                continue

            # has the photo owner blocked this user
        
            if not blocked_by.has_key(photo_owner) :
                is_blocked = Blocked.is_user_blocked(ctx.user.nsid, photo_owner)
                blocked_by[photo_owner] = is_blocked

            if blocked_by[photo_owner] :
                continue
        
            filtered.append(ph)

        if len(filtered) == 0 :
            ctx.api_error(3, 'Retry, no photos post filter');   
            return
        
        rsp['photos']['photo'] = filtered

        ctx.api_ok({'photos' : rsp['photos']})
        return

class SearchForUserHandler (CoreHandler) :

    def run (self, ctx) :
        
        required = ('user_id',)

        if not ctx.ensure_args(required) :
            return 

        per_page = 100
        page = ctx.request.get('page')
                       
        method = 'flickr.photos.search'
        
        args = {
            'user_id' : ctx.request.get('user_id'),
            'has_geo' : 0,
            'auth_token' : ctx.user.token,
            'extras' : 'tags,date_taken,owner_name',            
            'per_page' : per_page,
            'page' : page,
            }

        ttl = 60 * 10;

        rsp = ctx.proxy_api_call(method, args, ttl)
        
        # wrong and dirty, please to fix
        ctx.format = 'json'

        if not rsp or rsp['stat'] != 'ok' :
            ctx.api_error(1, 'API call failed')
            return

        if rsp['photos']['total'] == 0 :
            ctx.api_ok()
            return

        # it's assumed you've checked that the logged in
        # user hasn't been blocked by the searched for
        # user by now and that the searched for user hasn't
        # opted out

        # please to memcache me...
        
        gql = "SELECT * FROM dbSuggestion WHERE suggestor_nsid=:1"
        res = db.GqlQuery(gql, ctx.user.nsid)

        skip_photos = []
        filtered = []

        for ph in res.fetch(res.count()) :
            skip_photos.append(ph.photo_id)

        for ph in rsp['photos']['photo'] :

            if not long(ph['id']) in skip_photos :
                filtered.append(ph)

        if len(filtered) == 0 :
            ctx.api_error(2, 'Retry, no photos for filter')
    
        rsp['photos']['photo'] = filtered

        ctx.api_ok({'photos' : rsp['photos']})
        return
