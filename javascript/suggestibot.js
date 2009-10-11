if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.suggestify){
    info.aaronland.suggestify = {};
}

info.aaronland.suggestify.Suggestibot = function(args){
    this.args = args;
    this.rsp = null;

    var api_args = {
        'host' : this.args['suggestify_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    this.api = new info.aaronland.suggestify.API(api_args);
};

info.aaronland.suggestify.Suggestibot.prototype.approve = function(suggestion_id, photo_id){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

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

    // 

    var perms = $("input[name='geo_perms_" + suggestion_id + "']:checked").val();
    var context = $("input[name='geo_context_" + suggestion_id + "']:checked").val();

    var meth_args = {
        'crumb' : this.args['approve_crumb'],
        'geo_perms' : perms,
        'geo_context' : context,
        'photo_id' : this.args['robot_photo_id'],
        'lat' : this.args['robot_lat'],
        'lon' : this.args['robot_lon'],
        'acc' : this.args['robot_acc'],
        'context' : this.args['robot_context'],        
        '_s' : this.args['robot_sig'],
    };

    //

    var _self = this;

    var req = new XMLHttpRequest();
    var url = this.args['suggestify_apihost']  + '/robots/' + this.args['robot_uuid'];

    console.log(meth_args)

    var params = new Array();

    for (key in meth_args){
        params.push(encodeURIComponent(key) + '=' + encodeURIComponent(meth_args[key]));
    }
    
    params = params.join("&");
            
    req.open('POST', url, true);

    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.setRequestHeader("Content-length", params.length);
    req.setRequestHeader("Connection", "close");

    _onReadyState = function(e){
        if (req.readyState != 4){
            return;
        }

        // _self.log("api call (" + method + ") dispatch returned with HTTP status: " + req.status);

        if (req.status != 200){
            // _self.log("api call failed: " + req.responseText);

            if (doThisIfNot){
                doThisIfNot();
            }

            return;
        }

        var rsp;
        var stat;

        if (req.responseXML){
            var doc = req.responseXML;
            rsp = doc.getElementsByTagName("rsp")[0];
            stat = rsp.getAttribute("stat")
        }

        else if (typeof(JSON) == 'object') {
            var txt = req.responseText;
            var json = JSON.parse(txt);
            rsp = json['rsp'];
            stat = rsp['stat'];
        }
        
        else {
            // _self.log("uhh...there's neither any XML to parse or a JSON parser to parse with. freaking out...");
            return;
        }

        // _self.log("api call (" + method + ") dispatch returned with API status: " + stat);

        if ((stat == 'ok') && (doThisOnSuccess)){
            doThisOnSuccess(rsp);
        }

        else if (doThisIfNot){
            doThisIfNot(rsp);
        }

        else {
            // _self.log("no API callbacks defined for method call (" + method + "), oh well...");
        }
    };

    req.onreadystatechange = _onReadyState;
    req.send(params);  

    //

    this.showWhirClick(suggestion_id);
    return;    
};

info.aaronland.suggestify.Suggestibot.prototype.reject = function(suggestion_id){

    var html = '<span class="reject_ok">'
    html += 'OK! That suggestion has been rejected';
    html += '</span>';
    
    $("#whirclick_" + suggestion_id).html(html);
    return;    
};

info.aaronland.suggestify.Suggestibot.prototype.block = function(suggestion_id, suggestor_id){

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

info.aaronland.suggestify.Suggestibot.prototype.showWhirClick = function(suggestion_id){
    $("#approve_" + suggestion_id).hide();
    $("#reject_" + suggestion_id).hide();
    $("#tweak_" + suggestion_id).hide();
    $("#block_" + suggestion_id).hide();
    $("#showme_" + suggestion_id).hide();
    $("#whirclick_" + suggestion_id).show();
};

info.aaronland.suggestify.Suggestibot.prototype.showMap = function(lat, lon, zoom){
    window.iamheremap.goTo(lat, lon, zoom);
    $("#iamheremap_reviewcontainer").show();
    $("#iamheremap_review").show();
};

info.aaronland.suggestify.Suggestibot.prototype.hideMap = function(){
    $("#iamheremap_reviewcontainer").hide();
    $("#iamheremap_review").hide();
};

// -*-java-*-