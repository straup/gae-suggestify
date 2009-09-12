if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.suggestify){
    info.aaronland.suggestify = {};
}

info.aaronland.suggestify.Utils = function(){
    
};

info.aaronland.suggestify.Utils.prototype.scrub = function(str, allow_whitespace){

    str = encodeURIComponent(str);

    if (allow_whitespace){
        str = str.replace(/%20/g, " ");
    }

    return str;
};

