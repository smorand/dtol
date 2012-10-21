/**
 * This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
 */

$.fn.checkbox = function(checked) {
    for (var i = 0; i < $(this).length; i++) {
        var id = $(this).get(i).id;
        $('#' + id).after('<input type="hidden" id="checkbox-' + id + '" name="' + id + '" value="' + (checked ? 1 : 0) + '"/>');
    }
    var ev = function() {
	var img = $('#' + this.id + ' > img').get(0)
        if (img.src.indexOf('checkbox.gif') != -1) {
            img.src = img.src.replace('checkbox.gif', 'checkbox-checked.gif');
            $('#checkbox-' + this.id).val(1);
        } else {
            img.src = img.src.replace('checkbox-checked.gif', 'checkbox.gif');
            $('#checkbox-' + this.id).val(0);
        }
    };
    $(this).click(ev);
    $(this).keypress(function(e) {
        if (e.keyCode != 9) ev();
    });
}

$.fn.radio = function(checked, onChangeEvent) {
    var ev = function() {
        var related = $('img[name=' + this.name + ']');
        for (var i = 0; i < related.length; i++) {
            related.get(i).src = related.get(i).src.replace('radio-checked.gif', 'radio.gif');
        }
        this.src = this.src.replace('radio.gif', 'radio-checked.gif');
        $('#radio-' + related.get(0).name).val(this.id.substr(this.id.lastIndexOf('_')+1));
        if (onChangeEvent) {
        	onChangeEvent();
        }
    };
    $(this).click(ev);
    $(this).keypress(function(e) {
        if (e.keyCode != 9) ev();
    });
    var checkRadio = $('#' + $(this).get(0).name + '_' + checked);
    if (checkRadio.get(0)) {
        checkRadio.get(0).src = checkRadio.get(0).src.replace('radio.gif', 'radio-checked.gif');
    }
    checkRadio.before('<input type="text" style="display:none" id="radio-' + $(this).get(0).name + '" name="' + $(this).get(0).name + '" value="' + checked + '"/>');
}

function Dialog(name) {
	this.id = '#' + name;
	
	if (!$(this.id).length) {
		$('body').append('<div id="' + name + '" class="dialogBox"></div>');
	}
	
	this.create = function(params) {
		if (params.content) {
			$(this.id).html(params.content);
		}
		params.autoOpen = true;
		$(this.id).dialog(params);
                this.created = 1;
                $('button').removeClass().addClass('dtbutton');
	}
	
	this.close = function() {
		$(this.id).dialog('close');
	}

	this.open = function() {
		$(this.id).dialog('open');
                $('button').removeClass().addClass('dtbutton');
	}

	this.destroy = function() {
                if (this.created == 1) {
                    this.created = 0;
                    $(this.id).dialog('destroy');
                }
	}

	this.enable = function() {
		$(this.id).dialog('enable');
	}

	this.disable = function() {
		$(this.id).dialog('disable');
	}

	this.top = function() {
		$(this.id).dialog('moveToTop');
	}

	this.setOption = function(name, value) {
		$(this.id).dialog("option", name, value);
	}

	this.getOption = function(name) {
		return $(this.id).dialog("option", name);
	}

	this.addListener = function(event, func) {
		$(this.id).bind(event, func);
	}
	
}
