/**
 * This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
 */

/**
 * Variables
 */
var currentMenu = '';

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
	load_menu(window.location.hash.substring(1));
	setInterval(function checknav() {
		var newhash = window.location.hash.substring(1);
		if (currentmenu != newhash) {
			load_menu(newhash);
			currentmenu = newhash;
		}
	}, 100);

	
	//setTimeout('getUsersConnected()', 5000);
	setTimeout('recvChat()', 1000);
	
	$('#dialog_sponsor').dialog({
		autoOpen: false,
		width: 400,
		buttons: [
		    {
		    	text: translate("SAVE"), 
			click: function() {
				$('#profile_updateanswer').html('<img style="vertical-align: middle" src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SPONSORING") + '<br/>');
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
var currentmenu = window.location.hash.substring(1);
function load_menu(menuInfo) {
	var menuName = menuInfo.replace(/\/.*/, '');
	if (menuName != "tournaments" && menuName != "admin" && menuName != "teams" && menuName != "statistics" && menuName != "profile" && menuName != "game" && menuName != "logout" && menuName != "sponsor") {
		menuName = "challenges";
	}
	var args = menuInfo.substring(menuName.length+1);
	method = menuName
	$('.dtmenu').removeClass('dtmenuselected');
	$('#menu_' + menuName).addClass('dtmenuselected');
	currentMenu = method;
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
function load_challenges(args) {
	if (args && args == 'create') {
		load_challengecreate();
	} else {
		display_wait();
		$.get('/challenges', function(content) {
			display_content(content);
		});
	}
}

/**
 * Load constraints teams
 */
function load_teamsconstraints() {
	display_wait();
	currentmenu = window.location.hash = '#teams/constraints';
	$.get('/teams/constraints', function(content) {
		display_content(content);
	});
}

/**
 * Load constraints teams
 */
var createTeamElements = new Array();
function load_teamcreate() {
	display_wait();
	currentmenu = window.location.hash = '#teams/create';
	$.get('/teams/create', function(content) {
		display_content(content);
		load_teamcreateedit_callback();
	});
}

function load_teamrandom() {
	display_wait();
	currentmenu = window.location.hash = '#teams/random';
	$.get('/teams/random', function(content) {
		display_content(content);
		$('a.checkbox').checkbox(1);
	});
}


/** callback to create or edit team */
function load_teamcreateedit_callback() {
	$('[name=spawnstypes]').radio(1, displaySpawnTypes);
	$('.checkbox').checkbox();
	$('.filter_object').hide();
	$('.filter_room').hide();
	$('.filter_character').show();
	createTeamElements = new Array();
	createTeamElements['characters'] = new Array();
	createTeamElements['objects'] = new Array();
	createTeamElements['rooms'] = new Array();
	var chars = $('[name=characterdef]').each(function(i,e) {
		var def = $(e).val().split('|');
		createTeamElements['characters'][i] = {
			id: def[0],
			name: def[1],
			label: def[2],
			extensions: def[3].split('-'),
			filters: def[4].split('-'),
			force: def[5],
			deplacement: def[6]
		}
	});
	var objects = $('[name=objectdef]').each(function(i,e) {
		var def = $(e).val().split('|');
		createTeamElements['objects'][i] = {
			id: def[0],
			name: def[1],
			label: def[2],
			extensions: def[3].split('-'),
			filters: def[4].split('-')
		}
	});
	var rooms = $('[name=roomdef]').each(function(i,e) {
		var def = $(e).val().split('|');
		createTeamElements['rooms'][i] = {
			id: def[0],
			name: def[1],
			label: def[2],
			extensions: def[3].split('-'),
			filters: def[4].split('-')
		}
	});
}

function displaySpawnTypes() {
	$('.filter_character').hide();
	$('.filter_object').hide();
	$('.filter_room').hide();
	var st = $('#radio-spawnstypes').val();
	if (st == 1) {
		$('.filter_character').show();
	} else if (st == 2) {
		$('.filter_object').show();
	} else if (st == 3) {
		$('.filter_room').show();
	}
}

/**
 * Load challenge page
 */
function load_admin(userId) {
	if (userId) {
		$.get('/user/view/' + userId, editUser_callback);
	} else {
		display_wait();
		currentmenu = window.location.hash = '#admin';
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
	} else if (args && args == 'create') {
		load_teamcreate();
	} else if (args && args == 'random') {
		load_teamrandom();
	} else if (args && args.match('^edit/[1-9][0-9]*$')) {
		load_teamedit(args.replace('edit/', ''));
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

var createdeficontent = ''; 
function createteamconstraint(keepcontent) {
	var createdeficontenttmp = '';
	if (keepcontent) {
		createdeficontenttmp = $('#content').html();	
	}
	editteamconstraint(0, keepcontent);
	if (keepcontent) {
		createdeficontent = createdeficontenttmp;
	}	
}
function editteamconstraint(id, keepcontent) {
	createdeficontent = '';
	display_wait();
	$.get('/teams/constraints/edit/' + id + '/' + (keepcontent ? '1' : '0'), function(content) {
		display_content(content);
		$('.accordion').accordion({
			collapsible: true,
			active: 0,
			autoHeight: false
		});
		var extensions = $.trim($('#tc_extensions').val()).split(',');
		for (var i = 0; i < extensions.length; i++) {
			selectExtension($.trim(extensions[i]));
		}
		if (keepcontent) {
			$('#tc_gamelink').val(1);
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
	$('#profile_updateanswer').html('<img style="vertical-align: middle" src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SAVING") + '<br/>');
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
	$('#profile_updateanswer').html('<img style="vertical-align: middle" src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SAVING") + '<br/>');
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
function selectExtension(id, callback) {
	$('#extlogo_' + id).toggleClass('extensionlogo-selected');
}

/**
 * select extension for registration
 */
function selectExtensionAll() {
	$('.extensionlogo-notselected').addClass('extensionlogo-selected');
}


/**
 * select extension for registration
 */
function selectExtensionNone() {
	$('.extensionlogo-selected').toggleClass('extensionlogo-selected');
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
	$('#userlist').html('<img style="vertical-align: middle" src="/static/images/interface/loading.gif"/>&nbsp;' + translate("ACTION_IN_PROGRESS") + '<br/>')
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
	var extensions = $.trim($('#profile_extensions').val()).split(',');
	for (var i = 0; i < extensions.length; i++) {
		selectExtension($.trim(extensions[i]));
	}
}

function editUser(userId) {
	currentmenu = window.location.hash = '#admin/' + userId;
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
		var messages = $.trim(content).split('[|][$][|]');
		lastChatId = $.trim(messages[0]) > lastChatId ? $.trim(messages[0]) : lastChatId; 
		var chat = document.getElementById('chat');
		if (chat) {
			if (messages[1] == '1' && firstScroll == false) {
				if (headerIsVisible == 0) toggleheader()
				$('.header-chat').show();
			}
			var autoscroll = firstScroll || chat.scrollTop+chat.offsetHeight >= chat.scrollHeight-5;
			firstScroll = false;
			if (messages[2]) {
				chat.innerHTML += $.trim(messages[2]);
			}
			if (autoscroll == true) {
				chat.scrollTop = chat.scrollHeight + chat.offsetHeight;
			}
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
	var fields = $.trim(rawdata).split('|')
	for (i = 0; i < fields.length; i++) {
		var info = $.trim(fields[i]).split('=');
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
	var tcname = $('#tc_name').val();
	$('#tc_extensions').val(extsString);
	var form = $('#tc_form');
	$.post(form.attr('action'), form.serialize(), function(content) {
		if (content.length == 0) {
			if (createdeficontent != '') {
				display_content(createdeficontent);
				updatecreatedeficonstraint(tcname);
				createdeficontent = '';
			} else {
				load_teamsconstraints();
			}
		} else {
			$('#tc_error').html(content);
		}
	});
	return false;
}

/** Update the constraint for challenge creation */
function updatecreatedeficonstraint(tcname) {
	$.get('/teams/constraints/loadbyname/'+tcname, function(content) {
		$('#constraint_list').html(content);
	});
}

/**
 * Runfilter for team creation
 */
var spawnSelected = new Array();
function runcreateteamfilter(typin) {
	var directory = 'spawns';
	var fileext = '.png';
	var typ = $('#radio-spawnstypes').val();
	if (typin) typ = typin;
	if (typ == 1) {
		typ = 'character';
	} else if (typ == 2) {
		typ = 'object';
	} else if (typ == 3) {
		typ = 'room';
		directory = 'rooms';
		fileext = '.jpg';
	}
	
	var exts = new Array();
	$('.extensionlogo-selected').each(function(i,e) {
		exts[exts.length] = $(e).attr('id').split('_')[1];
	});

	spawnSelected = new Array();
	if (exts.length > 0) {
		$('#teamspawndisplay').html('<center><img src="/static/images/interface/loading.gif"/><br/>' + translate("LOADING_SPAWN") + '</center>');
		// check filter selected none => all, one or several => only these one
		var filters = $('div.filter_'+typ+ ' > a');
		var filterslist = new Array();
		for (var i in filters) {
			a = filters[i];
			if (a.href) {
				if ($(a).find('img').attr('src').indexOf('checkbox-checked') > 0) {
					filterslist[filterslist.length] = a.id.replace('filter_', '');
				}
			}
		}
		// check spawn to select
		for (i = 0; i < createTeamElements[typ+'s'].length; i++) { var spawn = createTeamElements[typ+'s'][i];
			var found = 0;
			var e = 0;
			var f = 0;
			for (e = 0; e < spawn.extensions.length; e++) {
				for (f = 0; f < exts.length; f++) {
					if (spawn.extensions[e] == exts[f]) {
						found = 1;
						break;
					}
				}
				if (found) break;
			}
			if (found) {
				var checkfilter = 0;
				// Check deplacement and force for characters
				if (typ == 'character') {
					var val = parseInt($('#depmin').val())
					if (val != Number.NaN && spawn['deplacement'] < val) continue;
					var val = parseInt($('#depmax').val())
					if (val != Number.NaN && spawn['deplacement'] > val) continue;
					var val = parseInt($('#forcemin').val())
					if (val != Number.NaN && spawn['force'] < val) continue;
					var val = parseInt($('#forcemax').val())
					if (val != Number.NaN && spawn['force'] > val) continue;
				}
				if (filterslist.length > 0) {
					for (var f in filterslist) {
						for (var c in spawn['filters']) {
							if (spawn['filters'][c] == filterslist[f]) {
								checkfilter = 1;
								break;
							}
						}
						if (checkfilter == 1) break;
					}
				} else {
					checkfilter = 1;
				}
				if (checkfilter == 1) {
					spawnSelected[spawnSelected.length] = { url: graphicsPack + '/static/images/' + directory + '/' + spawn['name'] + fileext, spawn: spawn };
					$.imagePreload(spawnSelected[spawnSelected.length-1]['url'], function() {createTeamDisplaySpawn(typ, spawnSelected);});
				}
			}
		}
	}
	
	if (spawnSelected.length > 0) {
		progressbarDialog = new Dialog('dialog_progressbar');
		$.runPreloading(function() {createTeamDisplaySpawn(typ, spawnSelected);});
	} else {
		$('#teamspawndisplay').html('<center><img src="/static/images/interface/forbidden.gif"/><br/>' + translate("NO_SPAWN_SELECTED") + '</center>');
	}
}

/** Appelée quand la sélection des pions est effectuée et que les pions sont chargés pour l'affichage. Utilise spawnSelected */
var createteamid = 0;
function createTeamDisplaySpawn(typ, spawnSelected) {
	$('#teamspawndisplay').html('');
	var i = 0;
	for (i = 0; i < spawnSelected.length; i++) {
		if (typ == 'room') {
			$('#teamspawndisplay').append('<div class="iconcontainer"><img height="200" width="200" src="' + spawnSelected[i]['url'] + '" border="0" class="pointer" onclick="selectionTeamSpawn(\'' + typ + '\', \'' + spawnSelected[i]['spawn']['name'] + '\', ' + spawnSelected[i]['spawn']['id'] + ')"/></div> ');
		} else {
			createteamid++;
			if (useExcanvas) {
				$('#teamspawndisplay').append('<div class="iconcontainer"><img height="80" width="80" src="/spawn/' + $('#spawncolor').val() + '/' + spawnSelected[i]['spawn']['name'] + '" border="0" class="pointer" onclick="selectionTeamSpawn(\'' + typ + '\', \'' + spawnSelected[i]['spawn']['name'] + '\', ' + spawnSelected[i]['spawn']['id'] + ')"/></div>');
			} else {
				$('#teamspawndisplay').append('<div class="iconcontainer"><canvas id="createteamicon_' + createteamid + '" height="80" width="80" border="0" class="pointer" onclick="selectionTeamSpawn(\'' + typ + '\', \'' + spawnSelected[i]['spawn']['name'] + '\', ' + spawnSelected[i]['spawn']['id'] + ')"/></div>');
				var canvas = $('#createteamicon_' + createteamid);
				var ctx = canvas.get(0).getContext('2d');
				var img1 = new Image();
				img1.src = '/static/images/spawns/fond-' + $('#spawncolor').val() + '.png';
				ctx.drawImage(img1, 0, 0, 80, 80);
				var img2 = new Image();
				img2.src = spawnSelected[i]['url']
				ctx.drawImage(img2, 0, 0, 80, 80);
			}
		}
	}
	progressbarDialog.destroy();
}

/** Bascule le mode aide */
var displayHelp = 0;
function toggleHelp() {
	if (displayHelp == 0) {
		$('#togglehelp').attr('src', '/static/images/interface/help.png');
		displayHelp = 1;
	} else {
		$('#togglehelp').attr('src', '/static/images/interface/helpno.png');
		displayHelp = 0;
	}
}

/** Sélection d'un pion d'équipe */
function selectionTeamSpawn(typ, name, id, force) {
	if (typ == 'room') name = name.split('-')[0];
	if (displayHelp == 1 && !force) {
		$('#actionsdialog').html('');
		$.get('/spawn/help/' + typ + '/' + id, function(content) {
			$('#actionsdialog').html(content);
			$('#actionsdialog').dialog({
				autoOpen: true,
				width: 300,
				title: translate('HELP_TITLE') + "&nbsp;-&nbsp;" + $('#spawnhelpname').val()  + '&nbsp;' + '<img class="pointer" width="20" height="20" border="0" style="vertical-align:middle" src="/static/images/interface/plus.png" onclick="selectionTeamSpawn(\'' + typ + '\', \'' + name + '\', \'' + id + '\', 1)"/>'
			});
		});
	} else {
		$('#panier_'+typ+'s').val($('#panier_'+typ+'s').val() +id+'_'+name+',');
		try {
			$('#actionsdialog').dialog('destroy');
		} catch(ex) { /**/ }
	}
	teamContent();
}

/** Mets à jour le contenu de l'équipe */
function unselectionTeamSpawn(typ, name) {
	var spawns_str = $('#panier_'+typ+'s').val();
	var spawnalreadyremoved = false;
	var newval = '';
	var spawncount = 0;
	if (spawns_str.length > 0) {
		var spawns = spawns_str.split(',');
		for (var c in spawns) { var spawn = spawns[c];
			if ((spawn.length > 0 && spawn != name) || spawnalreadyremoved) {
				newval += spawn + ',';
			} else {
				spawnalreadyremoved = true;
			}
		}
		$('#team_'+typ+'scount').html(spawncount)
	}
	$('#panier_'+typ+'s').val(newval);
	teamContent();
}

/** Mets à jour le contenu de l'équipe */
var teampcontentid = 0;
function teamContent() {
	var types = new Array();
	types[types.length] = 'character';
	types[types.length] = 'object';
	types[types.length] = 'room';
	var content = '';
	var atleastonespawn = 0;
	$('#teamsdialog').html('');
	for (var t in types) { var typ = types[t];
		var spawns_str = $('#panier_'+typ+'s').val();
		var spawncount = 0;
		if (spawns_str.length > 0) {
			var spawns = spawns_str.split(',');
			for (var c in spawns) { var spawn = spawns[c];
				if (spawn.length > 0) {
					atleastonespawn = 1;
					spawncount++;
					var info = spawn.split('_');
					if (typ == 'room') {
						$('#teamsdialog').append('<div class="iconcontainer"><img height="150" width="150" src="/static/images/rooms/' + info[1] + '-1.jpg" border="0" class="pointer" onclick="unselectionTeamSpawn(\'' + typ + '\', \'' + spawn + '\')"/></div><div class="iconcontainer"><img height="150" width="150" src="/static/images/rooms/' + info[1] + '-2.jpg" border="0" class="pointer" onclick="unselectionTeamSpawn(\'' + typ + '\', \'' + spawn + '\')"/></div>');
					} else {
						if (useExcanvas) {
							$('#teamsdialog').append('<div class="iconcontainer"><img height="80" width="80" src="/spawn/' + $('#spawncolor').val() + '/' + info[1] + '" border="0" class="pointer" onclick="unselectionTeamSpawn(\'' + typ + '\', \'' + spawn + '\')"/></div>');
						} else {
							teampcontentid++;
							$('#teamsdialog').append('<div class="iconcontainer"><canvas id="teamcontent_' + teampcontentid + '" height="80" width="80" border="0" class="pointer" onclick="unselectionTeamSpawn(\'' + typ + '\', \'' + spawn + '\')"/></div>');
							var canvas = $('#teamcontent_' + teampcontentid);
							var ctx = canvas.get(0).getContext('2d');
							var img1 = new Image();
							img1.src = '/static/images/spawns/fond-' + $('#spawncolor').val() + '.png';
							ctx.drawImage(img1, 0, 0, 80, 80);
							var img2 = new Image();
							img2.src = '/static/images/spawns/' + info[1] + '.png';
							ctx.drawImage(img2, 0, 0, 80, 80);
						}
					}
				}
			}
		}
		$('#team_'+typ+'scount').html(spawncount)
		$('#teamsdialog').append('<hr/>');
	}
	if (atleastonespawn == 1) $('#teamsdialog').append('<button class="dtbutton" onclick="saveTeam()">' + translate('TEAM_SAVE') + '</button>');
}

/** constraint help display */
function helpConstraint(id, name) {
	$('#actionsdialog').html('');
	$.get('/teams/constraints/help/' + id, function(content) {
		$('#actionsdialog').html(content);
		$('#actionsdialog').dialog({
			autoOpen: true,
			width: 500,
			title: translate('HELP_TITLE') + "&nbsp;-&nbsp;" + name
		});
	});
}

/** Monter l'équipe sélectionné */
function showTeam() {
	$('#teamsdialog').dialog({
		autoOpen: true,
		width: 860,
		title: translate('CURRENT_TEAM')  
	});	
}

/** Affichier l'équipe */
function displayTeam(id) {
	$.get('/teams/display/' + id, function(content) {
		$('#teamsdialog').html(content);
		showTeam();
		$('#teamsdialog').dialog('option', 'title', $('#displayteam_name').val())
	});
}

/** Enregistrer l'équipe */
function saveTeam() {
	var form = $('#teamCreateForm');
	$.post(form.attr('action'), form.serialize(), function(content) {
		if ($.trim(content) != '') {
			$('#teamCreateError').html(content);
		} else {
			load_teams();
		}
	});
}

/** Del team */
function delTeam(name, id) {
	if (confirm(translate('TEAM_CONFIRM_DELETE') + ' ' + name)) {
		$.get('/teams/remove/' + id, function(content) {
			load_teams();
		});
	}
}

/** Edit team */
function load_teamedit(id) {
	display_wait();
	currentmenu = window.location.hash = '#teams/edit/'+id;
	$.get('/teams/edit/' + id, function(content) {
		display_content(content);
		load_teamcreateedit_callback();
		teamContent();
	});
}

/** Run generation of random team */
function generateRandomTeam() {
	$('#randomteam_result').html('<img src="/static/images/interface/loading.gif"/><br/>' + translate("GENERATE_RANDOM_TEAM"));
	var form = $('#randomteam_form');
	var exts = $('.extensionlogo-selected')
	var extsString = '';
	var joiner = ''
	for (var i = 0; i < exts.length; i++) {
		extsString += joiner + exts.get(i).id.replace('extlogo_', ''); 
		joiner = ',';
	}
	$('#randomteam_extensions').val(extsString);
	$.post(form.attr('action'), form.serialize(), function(content) {
		$('#randomteam_result').html(content);
	});
	return false;
}

/** save a previously generated random teams(s) */
function saveRandomTeam() {
	$('#randomteamerr_result').html('<img style="vertical-align: middle" src="/static/images/interface/loading.gif"/>&nbsp;' + translate("SAVE_RANDOM_TEAM"));
	$.get('/teams/random/save', function(content) {
		$('#randomteamerr_result').html(content); 
	});
	return false;
}

/** Create a challenge */
function load_challengecreate() {
	display_wait();
	currentmenu = window.location.hash = '#challenges/create';
	$.get('/challenges/create', function(content) {
		display_content(content);
	});
}

/** Mise à jour des extensions lors de la création d'un challenge */
function updatechallengecreation() {
	var extsString = '';
	var joiner = '';
	var exts = $('.extensionlogo-selected');
	for (var i = 0; i < exts.length; i++) {
		extsString += joiner + exts.get(i).id.replace('extlogo_', ''); 
		joiner = ',';
	}
	$('#createchallenge_extensions').val(extsString);
}
