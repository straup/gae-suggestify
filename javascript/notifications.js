if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.suggestify){
    info.aaronland.suggestify = {};
}

// note: there is a very bad separation of form and content with the 
// notifications JS - the library is assuming all kinds of callbacks
// and class names that are happening at the template layer...

info.aaronland.suggestify.Notifications = function(args){
    this.args = args;

    var api_args = {
        'host' : this.args['suggestify_apihost'],
        'enable_logging' : this.args['enable_logging']
    };

    this.api = new info.aaronland.suggestify.API(api_args);
};

info.aaronland.suggestify.Notifications.prototype.enable_email = function(email_address){

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

info.aaronland.suggestify.Notifications.prototype.disable_email = function(){

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

info.aaronland.suggestify.Notifications.prototype.change_email = function(email_address){

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

info.aaronland.suggestify.Notifications.prototype.enable_comments = function(){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        var html = '<span class="toggle_comments_ok">';
        html += 'Okay! When someone suggests a location for one of your photos we\'ll post a notification comment on their behalf.';
        html += '</span>';

        $("#change_comments_status").html(html);
        $("#change_comments").hide();
    };

    var _doThisIfNot = function(rsp){

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="toggle_comments_fail">';
        html += 'Hrm. Robot central reported the following error: ' + msg;
        html += '</span>';

        $("#change_comments_status").html(html);
    };

    var meth_args = {
        'crumb' : this.args['comments_enable_crumb'],
    };
    
    this.api.api_call('enable_comments', meth_args, _doThisOnSuccess, _doThisIfNot);

    $("#change_comments_status").html('<span class="whirclick">robot squirrels are processing your request...</span>');
    $("#change_comments_status").show();
};

info.aaronland.suggestify.Notifications.prototype.disable_comments = function(){

    var _self = this;

    var _doThisOnSuccess = function(rsp){

        var html = '<span class="toggle_comments_ok">';
        html += 'Okay! You will no longer receive email notifications for new suggestions.';
        html += '</span>';

        $("#change_comments_status").html(html);
        $("#change_comments").hide();
    };

    var _doThisIfNot = function(rsp){

        var err = rsp.getElementsByTagName("error")[0];
        var msg = err.getAttribute("message");

        var html = '<span class="toggle_comments_fail">';
        html += 'Hrm. Robot central reported the following error: ' + msg;
        html += '</span>';

        $("#change_comments_status").html(html);
    };

    var meth_args = {
        'crumb' : this.args['comments_disable_crumb'],
    };
    
    this.api.api_call('disable_comments', meth_args, _doThisOnSuccess, _doThisIfNot);

    $("#change_comments_status").html('<span class="whirclick">robot squirrels are processing your request...</span>');
    $("#change_comments_status").show();
};

// -*-java-*-
