if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.suggestify){
    info.aaronland.suggestify = {};
}

info.aaronland.suggestify.JSON = (typeof(JSON) == 'object') ? 1 : 0;

info.aaronland.suggestify.API = function(args){
    this.args = args;

    this.host = args['host'];
    this.endpoint = '/api';

    if (! info.aaronland.suggestify.JSON){

        this.log("no native JSON parser, loading pure-js version");

        var script = document.createElement("script");
        script.setAttribute("type", "text/javascript");
        script.setAttribute("src", "/javascript/json2.js");

        var head = document.getElementsByTagName("head").item(0);
        head.appendChild(script);

        info.aaronland.suggestify.JSON = 1;
    }

};

info.aaronland.suggestify.API.prototype.api_call = function(method, args, doThisOnSuccess, doThisIfNot){

    var _self = this;

    var req = new XMLHttpRequest();
    var url = this.host + this.endpoint + '/' + encodeURIComponent(method); 

    var params = new Array();
    params.push('method=' + encodeURIComponent(method));

    for (key in args){
        params.push(encodeURIComponent(key) + '=' + encodeURIComponent(args[key]));
    }

    params = params.join("&");

    this.log("call " + url + ' with ' + params);

    req.open('POST', url, true);

    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.setRequestHeader("Content-length", params.length);
    req.setRequestHeader("Connection", "close");

    _onReadyState = function(e){
        if (req.readyState != 4){
            return;
        }

        _self.log("api call (" + method + ") dispatch returned with HTTP status: " + req.status);

        if (req.status != 200){
            _self.log("api call failed: " + req.responseText);

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
            _self.log("uhh...there's neither any XML to parse or a JSON parser to parse with. freaking out...");
            return;
        }

        _self.log("api call (" + method + ") dispatch returned with API status: " + stat);

        if ((stat == 'ok') && (doThisOnSuccess)){
            try {
                doThisOnSuccess(rsp);
            }
            catch (e){
                console.log(e);
            }
        }

        else if (doThisIfNot){
            doThisIfNot(rsp);
        }

        else {
            _self.log("no API callbacks defined for method call (" + method + "), oh well...");
        }
    };

    req.onreadystatechange = _onReadyState;
    req.send(params);

    this.log("api call dispatched");
};

info.aaronland.suggestify.API.prototype.log = function(msg){

    if (! this.args['enable_logging']){
        return;
    }

    if (typeof(console) != 'object'){
        return;
    }

    console.log('[api] ' + msg);
};