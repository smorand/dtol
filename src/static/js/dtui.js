/**
 * This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
 */
/**
 * Log function
 * @param msg Message to log
 */
$.log = function(msg) {
    var log = $('#log');
    if (log.length == 0) {
        // The log element does not exists, create it
        $('<div id="log" class="log"></div>').appendTo('body');
        log = $('#log');
    }
    log.html(msg + "<br/>\n" + log.html());
}

function translate(word) {
	return $('#translation-' + word).html();
}

/**
 * Change language
 */
function changeLang(lang) {
	$.post('/lang', { lang: lang }, function(content) {
		window.location.reload();
	});
}

function GetWidth() {
        var x = 0;
        if (self.innerHeight) {
                x = self.innerWidth;
        } else if (document.documentElement && document.documentElement.clientHeight) {
                x = document.documentElement.clientWidth;
        } else if (document.body) {
                x = document.body.clientWidth;
        }
        return x;
}

function onResize() {
	$('.header-chat').css('width', (GetWidth()-352)/2-30);
}

var headerIsVisible = 1;
function toggleheader() {
	if (headerIsVisible == 1) {
		$('.header').hide()
		$('#headerarrow').attr('src', '/static/images/interface/showheader.gif');
		headerIsVisible = 0;
	} else {
		$('.header').show()
		$('#headerarrow').attr('src', '/static/images/interface/hideheader.gif');
		headerIsVisible = 1;
	}
}

/**
 * This is the loading process.
 */
$(document).ready(function() {
	onResize();
	$(window).resize(onResize);
	$.History.bind(function(menuInfo) { load_menu(menuInfo); });
	load_menu(window.location.hash.substring(1));
	
	//setTimeout('getUsersConnected()', 5000);
	setTimeout('recvChat()', 1000);
	
	$('#dialog_sponsor').dialog({
		autoOpen: false,
		width: 400,
		buttons: [
		    {
		    	text: translate("SAVE"), 
			click: function() {
				$('#profile_updateanswer').html('<img src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SPONSORING") + '<br/>');
				$.get('/sponsor/' + $('#sponsor_email').val(), function(content) {
					$('#profile_updateanswer').html(content);
					$('#sponsor_email').val('');
				});
				$('#dialog_sponsor').dialog('close');
		        }
		    }		         
		]
	});
});

function getUsersConnected() {
	$.get('/user/connected', function(content) {
		$('#user-connected').html(content);
		setTimeout('getUsersConnected()', 5000);
	})
}

/**
 * Load one of the menu
 * @param menuName: Name of the menu to load
 */
function load_menu(menuInfo) {
	var menuName = menuInfo.replace(/\/.*/, '');
	if (menuName != "tournaments" && menuName != "admin" && menuName != "teams" && menuName != "statistics" && menuName != "profile" && menuName != "game" && menuName != "logout" && menuName != "sponsor") {
		menuName = "challenges";
	}
	var args = menuInfo.substring(menuName.length+1);
	method = menuName
	$('.dtmenu').removeClass('dtmenuselected');
	$('#menu_' + menuName).addClass('dtmenuselected');
	var toLoad = "load_" + method + "('" + args + "')";
	eval(toLoad);
}

/**
 * Load a menu from the id
 * @param src: Object source of the auto loading
 */
function load_automenu(src) {
	load_page(src.id.substring(5));
}

/**
 * Load a page
 */
function load_page(page) {
	if (window.location.hash == '#' + page) {
		load_menu(page);
	} else {
		window.location.hash = '#' + page;
	}
}

/**
 * Affiche un message d'attente de chargement de page
 */
function display_wait() {
	$('#content').html('<center><img src="/static/images/interface/loading.gif"/><br/>' + translate("LOADING") + '</center>');
}

/**
 * Load the content and parse forbidden page
 * @param content: The content itself
 */
function display_content(content) {
	$('#content').html(content);
}


/**
 * Load challenge page
 */
function load_challenges() {
	display_wait();
	$.get('/challenges', function(content) {
		display_content(content);
	});
}

/**
 * Load constraints teams
 */
function load_teamsconstraints() {
	display_wait();
	$.get('/teams/constraints', function(content) {
		window.location.hash = '#teams/constraints';
		display_content(content);
	});
}

/**
 * Load challenge page
 */
function load_admin(userId) {
	if (userId) {
		$.get('/user/view/' + userId, editUser_callback);
	} else {
		display_wait();
		window.location.hash = '#admin';
		$.get('/admin', display_content);
	}
}

/**
 * Load challenge page
 */
function load_tournaments() {
	display_wait();
	$.get('/tournaments', function(content) {
		display_content(content);
	});
}

/**
 * Load challenge page
 */
function load_teams(args) {
	if (args && args == 'constraints') {
		load_teamsconstraints();
	} else {
		display_wait();
		$.get('/teams', function(content) {
			display_content(content);
		});
	}
}

function delteamconstraint(id) {
	$.get('/teams/constraints/remove/' + id, function(content) {
		load_teamsconstraints();
	});
}

function createteamconstraint() { editteamconstraint(0); }
function editteamconstraint(id) {
	display_wait();
	$.get('/teams/constraints/edit/' + id, function(content) {
		display_content(content);
		$('.accordion').accordion({
			collapsible: true,
			active: 0,
			autoHeight: false
		});
		var extensions = $('#tc_extensions').val().trim().split(',');
		for (var i = 0; i < extensions.length; i++) {
			selectExtension(extensions[i].trim());
		}
	});
}

/**
 * Load challenge page
 */
function load_statistics(user) {
	display_wait();
	$.get('/statistics', function(content) {
		display_content(content);
	});
}

/**
 * Load challenge page
 */
function load_profile() {
	display_wait();
	$.get('/profile', function(content) {
		display_content(content);
		$('[name=menujeu]').radio($('#profile_ini_menujeu').val());
		var primarycolor = $('#profile_ini_primarycolor').val();
		var secondarycolor = $('#profile_ini_secondarycolor').val();
		$('[name=primarycolor]').radio(primarycolor, function() { checkProfileForm(); });
		$('[name=secondarycolor]').radio(secondarycolor, function() { checkProfileForm(); });
		updateSecondaryColor(primarycolor)
	});
}

/**
 * Load challenge page
 */
function load_game(args) {
	if (args.length == 0) {
		load_page('challenges');
	} else {
		display_wait();
		$.get('/game/' + args, function(content) {
			display_content(content);
		});
	}
}

/**
 * Logout
 */
function load_logout() {
	$.get('/logout', function(content) { window.location.reload(); });
}

/**
 * Sponsor
 */
function load_sponsor() {
	$('#dialog_sponsor').dialog('open');
}

/**
 * Hide the color group for the choice of the secondary color
 * @param color Color group to hide
 */
function updateSecondaryColor(color) {
	$('.fondgroupe').show();
	$('.fondgroupe' + color).hide();
}

/**
 * Check that password and confirm password are identical
 * @param selector Field selector 
 */
var colorGroup =  {
		'jaune': 1,
		'orange': 1,
		'bleu': 2,
		'cyan': 2,
		'rouge': 3,
		'violet': 3,
		'vert': 4,
		'vertflash': 4,
		'noir': 5,
		'marron': 5
};
function checkProfileForm() {
	if ($('#profile_password').val() != $('#profile_confirmpassword').val()) {
		$('#submit_profile').attr('disabled', true)
		$('#submit_profile').removeClass('dtbutton');
		$('#submit_profile').addClass('dtbutton-disabled');
		$('#passworddiffers').show();
	} else if (colorGroup[$('#radio-primarycolor').val()] == colorGroup[$('#radio-secondarycolor').val()]) {
		$('#submit_profile').attr('disabled', true)
		$('#submit_profile').removeClass('dtbutton');
		$('#submit_profile').addClass('dtbutton-disabled');
		$('#passworddiffers').hide();
	} else {
		$('#submit_profile').removeAttr('disabled')
		$('#submit_profile').removeClass('dtbutton-disabled');
		$('#submit_profile').addClass('dtbutton');
		$('#passworddiffers').hide();
	}
}

/**
 * Update profile 
 */
function updateProfile() {
	$('body').scrollTop(0);
	$('#profile_updateanswer').html('<img src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SAVING") + '<br/>');
	var form = $('#profile_form');
	var exts = $('.extensionlogo-selected')
	var extsString = '';
	var joiner = ''
	for (var i = 0; i < exts.length; i++) {
		extsString += joiner + exts.get(i).id.replace('extlogo_', ''); 
		joiner = ',';
	}
	$('#profile_extensions').val(extsString);
	$.post(form.attr('action'), form.serialize(), function(content) {
		$('#profile_updateanswer').html(content + '<br/>');
	});
}

/**
 * Update profile 
 */
function registerProfile() {
	$('#profile_updateanswer').html('<img src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SAVING") + '<br/>');
	var form = $('#profile_form');
	var exts = $('.extensionlogo-selected')
	var extsString = '';
	var joiner = ''
	for (var i = 0; i < exts.length; i++) {
		extsString += joiner + exts.get(i).id.replace('extlogo_', ''); 
		joiner = ',';
	}
	$('#profile_extensions').val(extsString);
	$.post(form.attr('action'), form.serialize(), function(content) {
		$('#profile_updateanswer').html(content + '<br/>');
		if (content.indexOf("message-error") == -1) {
			$('#profile_form').hide();
		}
	});
}

/**
 * select extension for registration
 */
function selectExtension(id) {
	$('#extlogo_' + id).toggleClass('extensionlogo-selected');
}

/**
 * Used to generate a password
 */
function generatePassword() {
	$('#dialog_generatepassword').dialog('open');
}

/**
 * Block/Unblock a user
 */
function toggleBlockUser(img, userId) {
	if (img.src.indexOf('ko') != -1) {
		value = 0;
		var newSrc = img.src.replace('ko', 'ok');
		var method = 'unblock'
	} else {
		value = 1;
		var newSrc = img.src.replace('ok', 'ko');
		var method = 'block'
	}
	$('#userlist').html('<img src="/static/images/interface/loading.gif"/>&nbsp;' + translate("ACTION_IN_PROGRESS") + '<br/>')
	$.get('/user/' + method + '/' + userId, function(content) {
		$('#userlist').html(content);
		img.src = newSrc;
	})
}

function becomeUser(userId) {
	$.get('/user/become/' + userId, function(content) {
		window.location.reload();
	});
}

function editUser_callback(content) {
	display_content(content);
	var primarycolor = $('#profile_ini_primarycolor').val();
	var secondarycolor = $('#profile_ini_secondarycolor').val();
	$('[name=primarycolor]').radio(primarycolor, function() { checkProfileForm(); });
	$('[name=secondarycolor]').radio(secondarycolor, function() { checkProfileForm(); });
	updateSecondaryColor(primarycolor);
	var extensions = $('#profile_extensions').val().trim().split(',');
	for (var i = 0; i < extensions.length; i++) {
		selectExtension(extensions[i].trim());
	}
}

function editUser(userId) {
	window.location.hash = '#admin/' + userId;
	display_content('<center><img src="/static/images/interface/loading.gif"/><br/>' + translate("LOAD_USER") + '</center>');
	$.get('/user/view/' + userId, editUser_callback);
}


/**
 * Envoi un message
 */
function postchat() {
	if ($('#chat_message').val() != '') {
		var form = $('#chat_form');
		$.post(form.attr('action'), form.serialize(), function() {
			$('#chat_message').val('');
		});
	}
	return false;
}

var firstChat = true;
function togglechat() {
	$('.header-chat').toggle()
	if (firstChat) {
		firstChat = false;
		var chat = document.getElementById('chat');
		chat.scrollTop = chat.scrollHeight + chat.offsetHeight;
	}
}


/** Reçoit les messages du chat */
var lastChatId = 0;
var firstScroll = true;
function recvChat() {
	$.get('/recvchat/' + lastChatId, function(content) {
		var messages = content.trim().split('|$|');
		lastChatId = messages[0].trim() > lastChatId ? messages[0].trim() : lastChatId; 
		var chat = document.getElementById('chat');
		if (messages[1] == '1' && firstScroll == false) {
			if (headerIsVisible == 0) toggleheader()
			$('.header-chat').show();
		}
		var autoscroll = firstScroll || chat.scrollTop+chat.offsetHeight >= chat.scrollHeight-5;
		firstScroll = false;
		chat.innerHTML += messages[2].trim();
		if (autoscroll == true) {
			chat.scrollTop = chat.scrollHeight + chat.offsetHeight;
		}
		setTimeout('recvChat()', 1000);
	});
}

/** Load constraint data for edition */
function loadconstraintdata() {
	$.get('/teams/constraints/load/' + $('#createconstraint_loadconstraint').val(), function(content) {
		loadformdata(content);
	});
}

/** Load data from a form to prefill another one */
function loadformdata(rawdata) {
	var fields = rawdata.trim().split('|')
	for (i = 0; i < fields.length; i++) {
		var info = fields[i].trim().split('=');
		// TODO: Better support for checkbox/radio
		if (info.length == 2) {
			$('#'+info[0]).val(info[1]);
		}
	}
}

/** Save a teams constraints */
function saveconstraintdata() {
	var exts = $('.extensionlogo-selected')
	var extsString = '';
	var joiner = ''
	for (var i = 0; i < exts.length; i++) {
		extsString += joiner + exts.get(i).id.replace('extlogo_', ''); 
		joiner = ',';
	}
	$('#tc_extensions').val(extsString);
	var form = $('#tc_form');
	$.post(form.attr('action'), form.serialize(), function(content) {
		if (content.length == 0) {
			load_teamsconstraints();
		} else {
			$('#tc_error').html(content);
		}
	});
	return false;
}
