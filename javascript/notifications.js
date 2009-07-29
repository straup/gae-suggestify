if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.geosuggestions){
    info.aaronland.geosuggestions = {};
}

info.aaronland.geosuggestions.Notifications = function(args){
    this.args = args;

    var api_args = {
        'host' : this.args['geosuggestions_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    this.api = new info.aaronland.geosuggestions.API(api_args);
};

info.aaronland.geosuggestions.Notifications.prototype.enable_email = function(email_address){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        var html = '<span class="new_email_ok">';
        html += 'Okay! Your email address has been registered. You should expect a confirmation email shortly.';
        html += '</span>';

        $("#new_email").html(html);
    };

    var _doThisIfNot = function(rsp){

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="new_email_fail">';
        html += 'Hrm. Your email address could not be registered. Robot central reported the following error: ' + msg;
        html += '</span>';

        $("#new_email").html(html);
    };

    var meth_args = {
        'crumb' : this.args['email_enable_crumb'],
        'email' : email_address,
    };
    
    this.api.api_call('enable_email', meth_args, _doThisOnSuccess, _doThisIfNot);

    $("#new_email_form").html('<span class="whirclick">robot squirrels are registering your email address</span>');
};

info.aaronland.geosuggestions.Notifications.prototype.disable_email = function(){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        var html = '<span class="disable_email_ok">';
        html += 'Okay! You will no longer receive email notifications for new suggestions.';
        html += '</span>';

        $("#disable_email").html(html);
        $("#change_email_listitem").hide();
    };

    var _doThisIfNot = function(rsp){

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="disable_email_fail">';
        html += 'Hrm. Robot central reported the following error: ' + msg;
        html += '</span>';

        $("#disable_email").html(html);
    };

    var meth_args = {
        'crumb' : this.args['email_disable_crumb'],
    };
    
    this.api.api_call('disable_email', meth_args, _doThisOnSuccess, _doThisIfNot);

    $("#disable_email_form").html('<span class="whirclick">robot squirrels are processing your request...</span>');
};

info.aaronland.geosuggestions.Notifications.prototype.change_email = function(email_address){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        var html = '<span class="change_email_ok">';
        html += 'Okay! Your new email address has been registered. You should expect a confirmation email shortly.';
        html += ' Until then, notifications will continue to be sent to your old email address.';
        html += '</span>';

        $("#change_email").html(html);
    };

    var _doThisIfNot = function(rsp){

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="change_email_fail">';
        html += 'Hrm. Your new email address could not be registered. Robot central reported the following error: ' + msg;
        html += '</span>';

        $("#change_email").html(html);
    };

    var meth_args = {
        'crumb' : this.args['email_change_crumb'],
        'email' : email_address,
    };
    
    this.api.api_call('enable_email', meth_args, _doThisOnSuccess, _doThisIfNot);

    $("#change_email_form").html('<span class="whirclick">robot squirrels are processing email address...</span>');
};

// -*-java-*-
