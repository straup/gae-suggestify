// this is not a generic buddyicon library
// it does not handle buddyicons for the logged in user
// maybe it should...

if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.geosuggestions){
    info.aaronland.geosuggestions = {};
}

info.aaronland.geosuggestions.Buddyicon = function(args){
    this.args = args;
    this.rsp = null;

    this.cache = {};

    var api_args = {
        'host' : this.args['geosuggestions_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    // hey look, we're using the local flickr proxy cache api

    this.api = new info.aaronland.geosuggestions.API(api_args);
};

info.aaronland.geosuggestions.Buddyicon.prototype.fetch = function(nsid, id){

    this.log("fetch buddyicon for " + nsid);
 
    var _self = this;

    if (this['cache'][nsid]){
        this.log('draw buddyicon from cache');
        this.draw(nsid, id, this['cache'][nsid]);
        return;
    }

    var _doThisOnSuccess = function (rsp){

        if (rsp['stat'] != 'ok'){
            _self.log('failed to retrieve people info for ' + nsid);
            return;
        }

        var buddyicon = 'http://farm' + rsp['person']['iconfarm'] + '.static.flickr.com/';
        buddyicon += rsp['person']['iconserver'];
        buddyicon += '/buddyicons/' + rsp['person']['nsid'] + '.jpg';

        _self.cache[nsid] = buddyicon;
        _self.draw(nsid, id, buddyicon);
    };

    var _doThisIfNot = function(rsp) { 
        _self.log("failed to fetch buddyicon for " + nsid);
    }

    var args = {
        'user_id' : nsid,
    };

    var method = 'flickr.people.getInfo';

    _self.api.api_call(method, args, _doThisOnSuccess, _doThisIfNot);
    return;
};

info.aaronland.geosuggestions.Buddyicon.prototype.draw = function(nsid, id, buddyicon_url){

        var html = '<a href="http://www.flickr.com/photos/' + escape(nsid) + '">';
        html += '<img src="' + buddyicon_url + '" height="32" width="32" alt="buddyicon" />';
        html += '</a>';

        $("#" + id).html(html);
};

info.aaronland.geosuggestions.Buddyicon.prototype.log = function(msg){

    if (! this.args['enable_logging']){
        return;
    }

    if (typeof(console) != 'object'){
        return;
    }

    console.log('[buddyicon] ' + msg);
};

// -*-java-*-