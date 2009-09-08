if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.info){
    info.aaronland.suggestify = {};
}

info.aaronland.suggestify.Chooser = function(args){
    this.args = args;
    this.rsp = null;
    this.search_index = null;
    this.current_index = null;

    var api_args = {
        'host' : this.args['suggestify_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    this.api = new info.aaronland.suggestify.API(api_args);
};

info.aaronland.suggestify.Chooser.prototype.lookupNSID = function(username){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        if (rsp['stat'] != 'ok'){

            var html = '<p style="color:red;font-weight:700;font-size:14pt;max-width:585px;">';
            html += 'Hrm. Flickr failed to find "' + escape(username) + '" and says: ' + rsp['message'] + '.';
            html += '</p>';
            html += '<p>Would you like to <a href="/chooser">try to find another user</a>?</p>';

            $("#photos").html(html);
            return;
        }

        var search_args = {
            'nsid' : rsp.user.nsid,
            'username' : username,
        };

        _self.photosSearch(search_args);
    };

    var _doThisIfNot = function (rsp) {

        var html = '<p style="color:red;font-weight:700;font-size:14pt;max-width:585px;">';
        html += 'Hrm. There was a problem fetching photos for <em>' + escape(username) + '</em>. ';
        html += 'Robot squirrels report "' + rsp['error']['message'] + '".';
        html += '</p>';
        html += '<p>Would you like to <a href="/chooser">try again</a>?</p>';

        $("#photos").html(html);
        return;
    };

    var method = 'flickr.people.findByUsername';

    var params = {
	'username' : username,
    };

    this.api.api_call(method, params, _doThisOnSuccess, _doThisIfNot);
};

info.aaronland.suggestify.Chooser.prototype.photosSearch = function(args){

    var _self = this;

    var _getItemHTML = function(photo){

        var uid = _self.generatePhotoUID(photo, 's');

        var url = [ 'http://farm', photo.farm, '.static.flickr.com/', photo.server, '/', photo.id, '_', photo.secret ].join('');    
        var img = '<img src="' + encodeURI(url) + '_s.jpg" width="75" height="75" alt="' + encodeURIComponent(photo.title) + '" id="' + uid  +'"';

	img += 'onclick="javascript:window.chooser.loadPhoto(' + encodeURIComponent(photo.id) + ');return false;" />';

        return img;
    };

    var _loadCarousel = function(carousel, state){
    
        for (var i = carousel.first; i <= carousel.last; i++) {

            if (carousel.has(i)) {
                continue;
            }

            if (i > _self.rsp.photos.perpage) {
                break;
            }

            var photo = _self.get_photo_by_offset((i - 1));

            if (! photo){
                break;
            }

            carousel.add(i, _getItemHTML(photo));
        }
    
    };

    var _doThisOnSuccess = function(rsp){

        console.log(rsp);

        // we really do reference this elsewhere
        _self.rsp = rsp;

        _self.build_search_index(rsp);

        var total = parseInt(rsp.photos.total);
        var size = parseInt(rsp.photos.perpage);

        if (! total){
            var html = '<p style="color:red;font-weight:700;font-size:14pt;max-width:585px;">';
            html += 'Hrm. The user "' + args['username'] + '" has no photos that are suitable for suggestification.';
            html += '</p>';
            html += '<p>Would you like to <a href="/chooser">try to find another user</a>?</p>';

            $("#photos").html(html);
            return;
        }

        var link = '<a href="http://www.flickr.com/photos/' + escape(args['nsid']) + '" style="text-decoration:none;">' + escape(args['username']) + '\'s</a>';
        var what = 'these are ' + link + ' (not geotagged) photos';
        $("#whatisthis_text").html(what);

        if (args['username']){
        	setTimeout(function(){
                	window.buddyicon.fetch(args['nsid'], 'whatisthis_icon');
        	}, 1500);
	}

        if (total < size){
            size = rsp.photos.total;
        }

        $("#photos").html("<ul></ul>");

        // this isn't quite right...

        var _onNext = function(foo, bar, canhas_next){

             if (canhas_next){
                    return;
             }

             var nsid = args['nsid'];
             var page = (args['page']) ? args['page'] + 1 : 2;
              _self.photosSearch({'nsid' : nsid, 'page' : page});
        };

        jQuery('#photos').jcarousel({
                'size' : size,
                'scroll':5,
                'visible':5,
                'itemLoadCallback': { onBeforeAnimation: _loadCarousel },
                // 'buttonNextCallback' : _onNext,
         });

        $("#whatisthis").show();
    };

    var _doThisIfNot = function (rsp){
        _self.log(rsp);
    };

    var method = 'search';

    this.api.api_call('search', { 'user_id' : args['nsid'], 'page' : args['page'] }, _doThisOnSuccess, _doThisIfNot);
};

info.aaronland.suggestify.Chooser.prototype.photosSearchRandom = function(){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        _self.rsp = rsp;

        var total = parseInt(rsp.photos.total);
        var size = parseInt(rsp.photos.perpage);

        if (! total){
            $("#options").html('There aren\'t any photos to suggest a location for!');
            return;
        }

        if (total < size){
            size = rsp.photos.total;
        }

        _self.build_search_index(rsp);

        var photo = _self.get_photo_by_offset(0);
        _self.loadPhotoRandom(photo);
    };

    var _doThisIfNot = function(rsp){
        $("#options").html("Ack! Bad craziness on the Information Superhighway means there are no photos to display!!");
        _self.log("photos search random failed!");
    };

    // fix me: pagination...

    this.api.api_call('random', { }, _doThisOnSuccess, _doThisIfNot);
}

info.aaronland.suggestify.Chooser.prototype.loadPhotoRandom = function(photo){

    	this.loadPhoto(photo);

        var html = '';

        html += '<ul id="options_random">';
        html += '<li id="options_random_skip">';
        html += '<a href="#" onclick="javascript:window.chooser.skip(' + encodeURIComponent(photo.id) + '); return false;">SKIP</a>';
        html += '</li>';
        html += '<li id="options_random_noidea">';
        html += '<a href="#" onclick="javascript:window.chooser.noIdea(' + encodeURIComponent(photo.id) + '); return false;">I HAVE NO IDEA</a>';
        html += '</li>';
        html += '</ul>';
        html += '<br clear="all" />';

        $("#options").html(html);
        return;
};

info.aaronland.suggestify.Chooser.prototype.loadPhoto = function(photo){

    if (typeof(photo) != 'object'){
        photo = this.get_photo_by_photoid(photo);
    }

    var uid = this.generatePhotoUID(photo);

    var url = [ 'http://farm', photo.farm, '.static.flickr.com/', photo.server, '/', photo.id, '_', photo.secret ].join('');    

    var photopage = 'http://www.flickr.com/photos/' + photo.owner + '/' + photo.id;

    var html = '<div style="float:left;">';

    html += '<strong>' + photo.title + '</strong>, by ' + photo.ownername;
    html += '<br />';
    html += '<em style="font-size:11px;">Date taken: ' + photo.datetaken + '</em>';
    html += '<br /><br />';

    html += '<a href="' + encodeURI(photopage) + '" target="not_here">';
    html += '<img class="current_photo" src="' + encodeURI(url) + '_m.jpg" alt="' + photo.title + '" id="' + escape(uid)  +'" />';
    html += '</a>';

    if (photo.tags != ''){
        html += '<br /><br />';
        html += 'Tagged with: <em>' + photo.tags.split(' ').join(', ') + '</em>';
    }

    if ((photo.tags != '') && (this.args['placemaker_apikey'])){
        html += '<br /><br />';
        html += '<div id="placemaker">';
        html += '<a href="#" onclick="javascript:window.chooser.queryPlacemaker(' + encodeURIComponent(photo.id) + ');return false;" class="tag_placemaker_link">';
        html += 'Try to determine photo location using tags?';
        html += '</a>';
        html += '</div>';
    }

    html += '<br /><br />';
    html += '<div id="suggestify">';
    html += 'Once you\'ve positioned the cross-hairs in the correct spot:<br />';
    html += '<a href="#" onclick="javascript:window.chooser.promptGeocode(' + encodeURIComponent(photo.id) + '); return false;" class="do_suggest_link">suggest this location</a>'; 
    html += '</div>';

    html += '<div id="confirmify"></div>';
    html += '</div>';

    html += '<br clear="all" />';
    html += '<div id="permalink" class="suggestion_permalink">this suggestion has a <a href="/chooser/photo/' + photo.id + '">permalink</a></div>';

    $("#foo").html(html);
};

info.aaronland.suggestify.Chooser.prototype.promptGeocode = function(photo_id, crumb){

    $("#suggestify").hide();
    $("#placemaker").hide();
    $("#permalink").hide();

    var map = window.iamheremap;
    var lat = map.lat.toFixed(3);
    var lon = map.lon.toFixed(3);

    html = 'The map is currently centered on ';
    html += 'latitude <strong>' + escape(lat) + '</strong> and longitude <strong>' + escape(lon) + '</strong>';
    html += ' at zoom level <strong>' + escape(map.zoom) + '</strong>.';

    if (map.woeid_name){
        html += ' In other words: ';
        html += map.woeid_name;
        html += '.';
    }

    html += '<br /><br />';
    html += 'This photo was taken:';
    html += '<br /><br />';

    html += '<form>';
    html += '<input type="radio" name="geo_context" value="1" /> indoors';
    html += '<input type="radio" name="geo_context" value="2" /> outdoors';
    html += '<input type="radio" name="geo_context" value="0" checked="true" /> who knows, who cares';
    html += '</form>';

    html += '<br />';
    html += '<em>Is this the location you want to suggest?</em>';

    html += '<br /><br />';
    html += '<div style="margin-left:25%;">';
    html += '<a href="#" onclick="javascript:window.chooser.Geocode(' + encodeURIComponent(photo_id) + '); return false;" class="confirm_geocode">YES</a>';
    html += '<a href="#" onclick="javascript:window.chooser.resetPromptGeocode(); return false;" class="confirm_geocode" style="background-color:#cc0066;">NO</a>';
    html += '<br clear="all" />';
    html += '</div>';

    $("#confirmify").html(html);
};

info.aaronland.suggestify.Chooser.prototype.resetPromptGeocode = function(photo_id){

    $("#confirmify").html("");
    $("#suggestify").show();
    $("#placemaker").show();
    $("#permalink").show();

    return;
};

info.aaronland.suggestify.Chooser.prototype.Geocode = function(photo_id){

    var photo = this.get_photo_by_photoid(photo_id);

    if (! photo){
        this.log("unable to locate photo object for id " + photo_id);
        return false;
    }

    var map = window.iamheremap;

    _doThisOnSuccess = function(rsp){

        $("#confirmify").hide();

        var html = '<span class="suggest_ok">';
        html += 'Yay! Your suggestion has been recordified!';
        html += '</span>';

        var s = $("#suggestify");
        s.html(html);
        s.show();
    };

    _doThisIfNot = function(rsp){

        $("#confirmify").hide();

        if (! rsp){
            alert("Hrm. Something went wrong calling the API!");
            return;
        }

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="suggest_fail">';
        html += 'Hrm. Suggestification failed with the following error: "' + msg + '"';
        html += '</span>';

        var s = $("#suggestify");
        s.html(html);
        s.show();

    };

    var api_args = {
        'host' : this.args['suggestify_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    var context = $("input[name='geo_context']:checked").val();

    var meth_args = {
        'photo_id' : photo['id'],
        'owner_id' : photo['owner'],
        'latitude' : map.lat,
        'longitude' : map.lon,
        'accuracy' : map.zoom,
        'woeid' : map.woeid,
        'geo_context' : context,
        'crumb' : this.args['suggest_crumb']
    };

    var api = new info.aaronland.suggestify.API(api_args);
    api.api_call('suggest', meth_args, _doThisOnSuccess, _doThisIfNot);

    $("#confirmify").html('<span class="whirclick">whir! click!!</span>');
    return;
};

// please to fix me to use info.aaronland.geo.Geocoder (placemaker)
// which is loaded by the iamheremap (20090907/asc)

info.aaronland.suggestify.Chooser.prototype.queryPlacemaker = function(photo_id){

    // http://icant.co.uk/jsplacemaker/

    if (! this.args['placemaker_apikey']){
        return;
    }

    var photo = this.get_photo_by_photoid(photo_id);

    if (! photo){
        return;
    }

    var _self = this;

    _onMatch = function(rsp){
        
        _self.log('placemaker dispatched returned');

        if (rsp.error){
            $("#placemaker").html("<em>Sorry, not able to figure out a place for those tags.</em>");
            return;
        }

        var match = rsp.match;
        var place = (typeof(match[0]) == 'undefined') ? match.place : match[0].place;

        var woeid = place.woeId;

        var lat = place.centroid.latitude;
        var lon = place.centroid.longitude;
        var zoom = 2;

        switch (place.type){
        	case 'Suburb' :
                    zoom = 14;
                    break;
        	case 'Town' :
                    zoom = 12;
                    break;
        	case 'County' :
                    zoom = 10;
                    break;
        	case 'State' :
                    zoom = 7;
                    break;
        	default :
                    zoom = 5;
                    break;
        }

        var map = window.iamheremap;
        map.goTo(lat, lon, zoom);

        $("#placemaker").html("best guess is " + place.name + ", which is a " + place.type);
    };

    this.log('query placemaker with: ' + photo.tags);

    $("#placemaker").html("<em>searching</em>");

    Placemaker.config.appID = this.args['placemaker_apikey'];
    Placemaker.getPlaces(photo.tags, _onMatch, 'en-us');

    this.log('placemaker query dispatched');
};

info.aaronland.suggestify.Chooser.prototype.generatePhotoUID = function(photo, sz){

    var uid = "photo_" + photo.id;

    if (sz){
        uid += sz;
    }

    return uid;
};

info.aaronland.suggestify.Chooser.prototype.skip = function(photo_id){

    this.log("skip " + photo_id);

    var photo = this.get_photo_by_offset((this.current_index + 1));    

    if (! photo){
        $("#options").html('<div id="loading">FETCHING MORE PHOTOS...</div>');
        this.photosSearchRandom();
        return;
    }

    this.loadPhotoRandom(photo);
};

info.aaronland.suggestify.Chooser.prototype.noIdea = function(photo_id){

    this.log("no idea where " + photo_id + " is");

    var _self = this;

    setTimeout(function(){
            var args = {
                'photo_id' : photo_id,
                'crumb' : _self.args['noidea_crumb']
            }

            _self.api.api_call('noidea', args, function (rsp) {}, function (rsp) {});
    }, 1500);

    this.skip(photo_id);
};

info.aaronland.suggestify.Chooser.prototype.build_search_index = function(rsp){

    this.search_index = {};
    this.current_index = null;

    var count = rsp.photos.photo.length;
    
    for (var i=0; i < count; i++){
        var id = rsp.photos.photo[i].id;
        this.search_index[ id ] = i;
    }
    
    return i;
};

info.aaronland.suggestify.Chooser.prototype.get_photo_by_offset = function(idx){

    this.log("get photo by offset: " + String(idx));

    if (! this.rsp){
        this.log("rsp is undefined!");
        return;
    }

    var photo = this.rsp.photos.photo[ idx ];
    
    this.current_index = Number(idx);
    return photo;
}

info.aaronland.suggestify.Chooser.prototype.get_photo_by_photoid = function(photo_id){

    this.log("get photo by id: " + String(photo_id));

    if (! this.rsp){
        this.log("rsp is undefined!");
        return;
    }

    if (! this.search_index){
        this.log("search index is undefined!");
        return;
    }

    var idx = this.search_index[ photo_id ];
    var photo = this.rsp.photos.photo[ idx ];

    this.current_index = Number(idx);
    return photo;
};

info.aaronland.suggestify.Chooser.prototype.log = function(msg){

    if (! this.args['enable_logging']){
        return;
    }

    if (typeof(console) != 'object'){
        return;
    }

    console.log('[chooser] ' + msg);
};

// -*-java-*-