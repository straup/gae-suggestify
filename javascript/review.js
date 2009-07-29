if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.geosuggestions){
    info.aaronland.geosuggestions = {};
}

info.aaronland.geosuggestions.Review = function(args){
    this.args = args;
    this.rsp = null;

    var flickr_args = {
        'key' : args['flickr_apikey'],
        'enable_logging' : args['enable_logging'],
    };

    this.flickr = new info.aaronland.flickr.API(flickr_args);

    var api_args = {
        'host' : this.args['geosuggestions_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    this.api = new info.aaronland.geosuggestions.API(api_args);
};

info.aaronland.geosuggestions.Review.prototype.approve = function(suggestion_id, photo_id){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        // TO DO:
        // a) redirect back to /review
        // b) remove all the other suggestions for photo id
        
        var photo_url = rsp.getAttribute('photo_url');

        var html = '<div class="approve_ok">';
        html += 'OK! Your photo has been geotagged!';
        html += '<div style="font-size:12pt;"><a href="';
        html += encodeURI(photo_url);
        html += '" style="text-decoration:none;color:darkslategrey;" target="_otherwindow">';
        html += 'Would you like to go see it now?</a>';
        html += '</div></div>';

        $("#whirclick_" + suggestion_id).html(html);

    };

    var _doThisIfNot = function(rsp){

        if (! rsp){
            alert("Hrm. Something went wrong calling the API!");
            return;
        }

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="approve_fail">'
        html += 'Hrm. Approval failed with the following error: "' + msg + '"';
        html += '</span>';

        var s = $("#whirclick_" + suggestion_id).html(html);
    };

    var perms = $("input[name='geo_perms_" + suggestion_id + "']:checked").val();
    var context = $("input[name='geo_context_" + suggestion_id + "']:checked").val();

    var meth_args = {
        'suggestion_id' : suggestion_id,
        'crumb' : this.args['approve_crumb'],
        'geo_perms' : perms,
        'geo_context' : context,
    };

    this.api.api_call('approve', meth_args, _doThisOnSuccess, _doThisIfNot);

    this.showWhirClick(suggestion_id);
    return;    
};

info.aaronland.geosuggestions.Review.prototype.reject = function(suggestion_id){

    var _doThisOnSuccess = function(rsp){

        var html = '<span class="reject_ok">'
        html += 'OK! That suggestion has been rejected';
        html += '</span>';

        $("#whirclick_" + suggestion_id).html(html);
    };
    
    var _doThisIfNot = function(rsp){

        if (! rsp){
            alert("Hrm. Something went wrong calling the API!");
            return;
        }

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="reject_fail">'
        html += 'Hrm. Rejection failed with the following error: "' + msg + '"';
        html += '</span>';

        var s = $("#whirclick_" + suggestion_id).html(html);
    };
    
    var meth_args = {
        'suggestion_id' : suggestion_id,
        'crumb' : this.args['reject_crumb']
    };

    this.api.api_call('reject', meth_args, _doThisOnSuccess, _doThisIfNot);

    this.showWhirClick(suggestion_id);
    return;    
};

info.aaronland.geosuggestions.Review.prototype.block = function(suggestion_id, suggestor_id){

    var _doThisOnSuccess = function(rsp){
        location.href = "/review?block=done";
    };

    var _doThisIfNot = function(rsp){

        if (! rsp){
            alert("Hrm. Something went wrong calling the API!");
            return;
        }

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="block_fail">';
        html += 'Hrm. Blocking failed with the following error: "' + msg + '"';
        html += '</span>'

        $("#whirclick_" + suggestion_id).html(html);
    };

    var meth_args = {
        'crumb' : this.args['block_crumb'],
        'user_id' : suggestor_id,
    };

    this.api.api_call('block', meth_args, _doThisOnSuccess, _doThisIfNot);

    this.showWhirClick(suggestion_id);
};

info.aaronland.geosuggestions.Review.prototype.showWhirClick = function(suggestion_id){
    $("#approve_" + suggestion_id).hide();
    $("#reject_" + suggestion_id).hide();
    $("#tweak_" + suggestion_id).hide();
    $("#block_" + suggestion_id).hide();
    $("#showme_" + suggestion_id).hide();
    $("#whirclick_" + suggestion_id).show();
};

info.aaronland.geosuggestions.Review.prototype.showMap = function(lat, lon, zoom){
    window.iamheremap.goTo(lat, lon, zoom);
    $("#iamheremap_reviewcontainer").show();
    $("#iamheremap_review").show();
};

info.aaronland.geosuggestions.Review.prototype.hideMap = function(){
    $("#iamheremap_reviewcontainer").hide();
    $("#iamheremap_review").hide();
};

// -*-java-*-