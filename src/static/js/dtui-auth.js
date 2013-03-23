/**
 * This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
 */
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

$(document).ready(function() {
	$('#dialog_generatepassword').dialog({
		autoOpen: false,
		width: 400,
		buttons: [
		    {
		    	text: translate("PASSWORD_GENERATION"), 
			click: function() {
			    	$('#password_generation').html('<img src="/images/interface/loading.gif"/>&nbsp;' + translate("PASSWORD_GENERATION_PROGRESS") + '<br/>');
				$.post('/generatepassword', { email: $('#generatepassword_email').val() }, function(content) {
					$('#password_generation').html(content);
					$('#generatepassword_email').val('');
				});
				$('#dialog_generatepassword').dialog('close');
		        }
		    }		         
		]
	});
});

/**
 * Used to generate a password
 */
function generatePassword() {
	$('#dialog_generatepassword').dialog('open');
}
