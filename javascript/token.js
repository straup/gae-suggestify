function confirm_token_change(id, ctx){

	if (ctx == 'review'){

		var html = '<div id="token_change_' + id + '">';
		html += '<span style="font-size:1.5em;">There\'s just one thing:</span><br /><br />';
		html += 'In order to review suggestions, the authentication token ';
		html += 'that connects your Flickr account with "suggestify" will need to be upgraded ';
		html += 'to have "write" permissions.<br /><br />';
		html += 'This is so that we can geotag a photo on your behalf ';
		html += 'when you approve a suggestion.<br /><br />';
		html += 'All that means is that when you click <q style="color:green;">OK</q> you\'ll be sent to Flickr and asked ';
		html += 'again to allow "suggestify" access to your account, only this time with ';
		html += '"write" permissions.<br /><br />';
		html += 'Once you do, you\'ll be sent back here to the list of suggestion awaiting your review.';
		html += '</div>';
		html += '<form method="GET" action="/review">';
		html += '<input type="submit" value="NEVERMIND. That\'s not what I want to do" onclick="skip_token_change(\'' + id + '\');return false" class="reject_token_change"/>';
		html += '<input type="submit" value="OK" class="confirm_token_change" />';
		html += '<br clear="all" />';
		html += '</form>';
	}

	else if (ctx == 'chooser'){

		var html = '<div id="token_change_' + id + '">';
		html += '<span style="font-size:1.5em;">There\'s just one thing:</span><br /><br />';
		html += 'If you\'d like to notify a person of a suggestion you\'ve made by leaving a comment ';
		html += 'on their photo, the authentication token ';
		html += 'that connects your Flickr account with "suggestify" will need to be upgraded ';
		html += 'to have "write" permissions.<br /><br />';
		html += 'All that means is that when you click <q style="color:green;">OK</q> you\'ll be sent to Flickr and asked ';
		html += 'again to allow "suggestify" access to your account, only this time with ';
		html += '"write" permissions.<br /><br />';
                html += 'Once you do, you\'ll be sent back here and you can suggestify like crazy.<br /><br />';
		html += '<em>Just remember that even if you have a token with "write" permissions the user whose photos your are ';
		html += 'suggesting locations for may have chosen to disallow comments from being added to their photos.</em>';
		html += '</div>';
		html += '<form method="GET" action="/chooser">';
		html += '<input type="hidden" name="perms" value="write">';
		html += '<input type="submit" value="I just want to suggest locations (never mind the comments)" onclick="skip_token_change_comments();return false;"';
		html += ' class="reject_token_change"/>';
		html += '<input type="submit" value="OK" class="confirm_token_change" />';
		html += '<br clear="all" />';
		html += '</form>';
	}

	else if (ctx == 'chooser_loggedout'){

		var html = '<div id="token_change_' + id + '">';
       		html += '<span style="font-size:1.5em;">There\'s just one thing:</span><br /><br />';
       		html += 'If you\'d like to notify a person of a suggestion you\'ve made by leaving a comment ';
              	html += 'on their photo, the authentication token ';
       		html += 'that connects your Flickr account with Suggestify will need ';
       		html += 'to have "write" permissions.<br /><br />';
              	html += 'You don\t need to do in order to create suggestions so if you\'d prefer that Suggestify ';
		html += 'only have a "read" access make sure to click the pink-ish button.';
		html += '<br /><br />';
               	html += '<em>Remember that even if you have a token with "write" permissions the user whose photos your are ';
                html += 'suggesting locations for may have chosen to disallow comments from being added to their photos.</em>';
               	html += '</div>';
               	html += '<form method="GET" action="/chooser">';
                html += '<input type="hidden" name="perms" value="write">';
               	html += '<input type="submit" value="Just a read-only token for now" onclick="skip_token_change_comments();return false;"';
                html += ' class="reject_token_change"/>';
               	html += '<input type="submit" value="A write token sounds good!" class="confirm_token_change" />';
               	html += '<br clear="all" />';
        	html += '</form>';
	}

        else {
            	return;            
        }

	$("#" + id).html(html);
}

// user does not want a 'write' token for leaving comment
// notifications so just issue a redirect

function skip_token_change_comments(){
	location.href='/chooser';
	return false;
}

// user doesn't want a 'write' token for reviewing suggestions
// so offer them something helpful to do in the meantime

function skip_token_change(id){

	var html = '<div id="token_skip">';
	html += 'Okay! We\'ll leave your "read" only Flickr authentication token in place';
	html += '</div>';

	if (id == 'main'){
		html += '<p>In the meantime, would you like to:</p>';
		html += '<ul class="options">';
		html += '<li><a href="/chooser">Suggestion a location</a></li>';
		html += '</ul>';
	}

	$("#" + id).html(html);
}

// user has clicked one of the links in the navi bar
// simply overwrite anything in div#main

function confirm_token_change_navi(ctx){
	confirm_token_change('main', ctx);
}

// user has clicked on the links from a list in div#main
// stick confirmation message in that

function confirm_token_change_list(ctx){
	id = ctx + "_link";
	confirm_token_change(id, ctx);
}
