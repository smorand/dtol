/**
 * This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
 */
/**
 * This is a OO library to interface DT with user action
 * This library is linked to jQuery free library
 * 
 */

/**
 * Current parameters of the library in the page
 */
var zoom = -1; // Zoom of the dungeon
var graphicsPack = ''; // Root directory or location for the image
var displayRotation = 0;
var currentScrollTop = 0;
var currentScrollLeft = 0;
var dialogAnimation = 0;

/**
 * Os detection information
 */
var agent = navigator.userAgent.toLowerCase();
var otherBrowser = (agent.indexOf("series60") != -1) || (agent.indexOf("symbian") != -1) || (agent.indexOf("windows ce") != -1) || (agent.indexOf("blackberry") != -1);
var mobileOS = typeof orientation != 'undefined' ? true : false;
var touchOS = ('ontouchstart' in document.documentElement) ? true : false;
var iOS = (navigator.platform.indexOf("iPhone") != -1) || (navigator.platform.indexOf("iPad") != -1) ? true : false;
var android = (agent.indexOf("android") != -1) || (!iOS && !otherBrowser && touchOS && mobileOS) ? true : false;
var tablettepc = mobileOS || touchOS || iOS || android;

/**
 * Temporary variables
 */
var referenceSize = 80; // This should never change if the same when zoom == 1
var imageToPreload = 0; // Image to preload
var imageToPreloadMax = 0; // Image to preload
var imgs = new Array(); // Image preloaded
var imgLoader = new Array(); // Used by the image preloader to create image object
var imgSrc = new Array(); // Used by the image preloader to store url
var spawnReduction = 5; // Spawn reduction for presentation
var selectBorderSize = 10; // Taille des réglettes
var currentDungeonDefinition = 0; // Taille du dongeon en nombre de salle
var progressbarDialog = 0; // Variable de progression pour le préchargement des images
var displayPosition = 0; // Si 1 les positions sont affichées

/**
 * Initialization
 */
function init_dungeon() {
	// Dialog
	$('#actionsdialog').dialog({
		autoOpen: true,
		width: 259,
		title: translate('GAME_LOADING')
	});
	$('#actionsdialog').html('<center><img border="0" src="/static/images/interface/loading.gif"/><br/>Chargement de la partie...</center>');
	$.get('/game/dungeon/1', function(content) {
		var dungeondef = eval('(' + content + ')');
		init_dungeon_callback(dungeondef);
	});
	$(window).scroll(function() {
		var st = $(window).scrollTop()
		var sl = $(window).scrollLeft()
		deltatop = st - currentScrollTop;
		deltaleft = sl - currentScrollLeft;
		var animationparam = {}
		if (deltaleft != 0) {
			animationparam.left = $('#actionsdialog').closest('.ui-dialog').offset().left+deltaleft;
		}
		if (deltatop != 0) {
			animationparam.top = $('#actionsdialog').closest('.ui-dialog').offset().top+deltatop;
		}
		dialogAnimation = $('#actionsdialog').closest('.ui-dialog').offset(animationparam);
		currentScrollTop = st;
		currentScrollLeft = sl;
	});
}

function init_dungeon_callback(dungeondefinitions) {
	displayRotation = dungeondefinitions.rotation;
	zoom = dungeondefinitions.zoom;
    progressbarDialog = new Dialog('dialog_progressbar');
    $('#zoom_slider').slider({
        min: 1,
        max: 15,
        step: 1,
        values: [0, zoom*10],
        range: true,
        slide: slide_callback,
        change: slide_callback
    });
    $('#zoom_slider a:first').hide();
    $('#dungeon_select').click(function(e) {
        // TODO : Detect button and what to do ?
        var height = $('#dungeon').attr('height')/(referenceSize*zoom);
        var width = $('#dungeon').attr('width')/(referenceSize*zoom);
        var positionMouse = $.getRelativePosition(e, 'dungeon_select');
        var res = { x: Math.floor(positionMouse.x/(referenceSize*zoom)), y: Math.floor(positionMouse.y/(referenceSize*zoom)) };
        // Select
        $('#dungeon_select').displaySelect(res);
    });
    $.setDungeonDefinition(dungeondefinitions);
    updateAction();
}

/** slide callback to set zoom */
function slide_callback(e, ui) {
	var cv = $('#zoom_slider').slider('option', 'values');
	if (cv[0] != 0) {
		$('#zoom_slider').slider('option', 'values', [0, cv[0]]);
	} else {
		zoom = ui.value/10.0;
		if (currentDungeonDefinition) {
		    $.displayDungeon();
		}
	}
}

/**
 * Set zoom
 * @param newZoom New zoom
 */
$.prototype.setZoom = function(newZoom) {
	var s = $('#zoom_slider').slider()
	s.slider('values', 1, newZoom*10);
}

/**
 * Effectue une rotation du dongeon
 * @param value valeur de la rotation (90°)
 */
$.prototype.dungonRotate = function(value) {
	displayRotation += value;
	displayRotation %= 4;
	// rotate current selection
	var dungeonDefinition = currentDungeonDefinition;
	if (locationSrc != 0) {
		var tmp = locationSrc.y;
		locationSrc.y = locationSrc.x;
		locationSrc.x = (displayRotation%2 == 1 ? dungeonDefinition.size.height : dungeonDefinition.size.width)*5+2 - tmp - 1;
	}
	if (locationDst != 0) {
		var tmp = locationDst.y;
		locationDst.y = locationDst.x;
		locationDst.x = (displayRotation%2 == 1 ? dungeonDefinition.size.height : dungeonDefinition.size.width)*5+2 - tmp - 1;
	}
	$.displayDungeon();
}

/**
 * 	Affiche les positions ou les caches
 * @param value valeur de la rotation (90°)
 */
$.dungonTogglePosition = function() {
	displayPosition++;
	displayPosition %= 2;
    $.displayPosition();
}

/**
 * Display position or clear position displaying
 */
$.displayPosition = function() {
    var dungeonDefinition = currentDungeonDefinition;
    var canvasPosition = $('#dungeon_position');
	if (displayPosition == 1) {
		// display position
		canvasPosition.get(0).getContext('2d').globalAlpha = 0.7;
	    for (var i in dungeonDefinition.rooms) { var room = dungeonDefinition.rooms[i]
	    	canvasPosition.displayPositionRoom(room);
	    	for (var x = 0; x < 5; x++) {
	    		for (var y = 0; y < 5; y++) {
	    			canvasPosition.displayPositionCase(room.position.x, room.position.y, x, y);
	    		}
	    	}

	    }
		$('#icon_displayposition').attr('src', '/static/images/interface/positionhide.png');
	} else {
		if (displayRotation % 2 == 0) {
			canvasPosition.get(0).getContext('2d').clearRect(0, 0, (dungeonDefinition.size.width*5+1)*referenceSize, (dungeonDefinition.size.height*5+1)*referenceSize);
		} else {
			canvasPosition.get(0).getContext('2d').clearRect(0, 0, (dungeonDefinition.size.height*5+1)*referenceSize, (dungeonDefinition.size.width*5+1)*referenceSize);
		}
		// hide position
		$('#icon_displayposition').attr('src', '/static/images/interface/position.png');
	}
}

/**
 * Set zoom
 * @param newZoom New zoom
 */
$.setDungeonDefinition = function(dungeonDefinition) {
    currentDungeonDefinition = dungeonDefinition;
    $.displayDungeon();
}

/**
 * Get the relative position of the mouse in an event element
 * @param e event
 */
$.getRelativePosition = function(e, eltId) {
    var t = $('#' + eltId).get(0);
    var x = e.pageX;
    var y = e.pageY;
    do {
    	x -= t.offsetLeft;
    	y -= t.offsetTop;
    } while (t = t.offsetParent);
    return {x:x,y:y};
}

/**
 * Function to add image to preload
 * @param url Url of the image to preload
 * @param fnc Function callback to call when preloading is over
 */
$.imagePreload = function(url, fnc) {
    if (!imgs[url]) {
        imageToPreload++;
        var img = new Image();
        $(img).load(function() {
            imageToPreload--;
            var val = 100-Math.round(imageToPreload*100/imageToPreloadMax);
            progressbarDialog.create({ title: 'Chargement en cours ...', content: '<div id="progressbar" class="progressbar"></div>', width: '350px' });
            $('#progressbar').progressbar({ value: val });
            if (imageToPreload == 0) {
            	$('[name=menubutton]').attr('class', 'dtmenu');
            	$('#menu_' + currentMenu).addClass('dtmenuselected');
                fnc();
            }
        });
        imgLoader[imgLoader.length] = img;
        imgs[url] = img;
        imgSrc[imgSrc.length] = url;
    }
}

/**
 * Run preloading of image
 */
$.runPreloading = function(fnc) {
    if (imgSrc.length > 0) {
        imageToPreloadMax = imageToPreload;
        progressbarDialog.create({ title: 'Chargement en cours ...', content: '<div id="progressbar" class="progressbar"></div>', width: '350px' });
        $('#progressbar').progressbar({ value: 0 });
        for (var i in imgSrc) {
            imgLoader[i].src = imgSrc[i];
        }
        imgLoader = new Array();
        imgSrc = new Array();
    } else {
    	$('[name=menubutton]').attr('class', 'dtmenu');
    	$('#menu_teams').addClass('dtmenuselected');
        fnc();
    }

}
/**
 * Display the dungeon in the current element. If the element is not a canvas, nothing is done
 * and an error is logged. The first part is to preload image and then to call the
 * displayDungeonLoadOver method wich will do the job
 * @param dungeonDefinition Definition of the dungeon
 * The dungeon definition should be:
 * {
 *   size: { width:, height: },
 *   rooms:
 *     [
 *       {
 *          position: { x: <int>, y: <int> },
 *          name: <int>-<1|2>,
 *          rotation: <0|1|2|3>,
 *          markers: { ... },
 *       }
 *     ],
 *   slides: [ { color: <string>, size: <int>, position: { x: <int>, y: <int> }, direction: <h|v> } ],
 *   spawns: [
 *      {
 *        name: <string>,
 *        room: { x:, y: }, // Could be empty, meaning this is an absolute position used for slides
 *        position: { x:, y: },
 *        states: [ <string> ]
 *      }
 *   ]
 */
$.displayDungeon = function() {
    var dungeonDefinition = currentDungeonDefinition;
    // Hide. TODO: Progress bar
    var canvasRooms = $('#dungeon_rooms');
    var canvasSpawns = $('#dungeon_spawns');
    canvasRooms.hide();
    canvasSpawns.hide();
    // Preload rooms
    for (var i in dungeonDefinition.rooms) { var room = dungeonDefinition.rooms[i];
        $.imagePreload(graphicsPack + '/static/images/rooms/' + room.name + '.jpg', function() {
            $.displayDungeonLoadOver(dungeonDefinition);
        });
        // TODO: Preload markers of rooms
    }
    // Prelod positions
    var positionsimages = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    for (var i in positionsimages) { var pos = positionsimages[i]; 
	    $.imagePreload(graphicsPack + '/static/images/rooms/position_' + pos + '.png', function() {
	        $.displayDungeonLoadOver(dungeonDefinition);
	    });
    }
    // Prelod slides
    $.imagePreload(graphicsPack + '/static/images/rooms/reglette.jpg', function() {
        $.displayDungeonLoadOver(dungeonDefinition);
    });
    for (var i in dungeonDefinition.slides) { var slide = dungeonDefinition.slides[i];
        $.imagePreload(graphicsPack + '/static/images/rooms/reglette-' + slide.color + '.png', function() {
            $.displayDungeonLoadOver(dungeonDefinition);
        });        
    }
    // Preload spawns
    for (var i in dungeonDefinition.spawns) { var spawn = dungeonDefinition.spawns[i];
        $.imagePreload(graphicsPack + '/static/images/spawns/' + spawn.name + '.png', function() {
            $.displayDungeonLoadOver(dungeonDefinition);
        });
        $.imagePreload(graphicsPack + '/static/images/spawns/fond-' + spawn.color + '.png', function() {
            $.displayDungeonLoadOver(dungeonDefinition);
        });
        for (var i in spawn.states) { var state = spawn.states[i];
        	if (state == 'consecrated' || state == 'undead' || state == 'bonusdefense' || state == 'bonusattaque' || state == 'noout' || state == 'cursed' || state == 'acidified' || state == 'poisoned' || state == 'hurt' || state == 'knocked' || state == 'tired' || state == 'freezed') {
		        $.imagePreload(graphicsPack + '/static/images/markers/' + state + '.png', function() {
		            $.displayDungeonLoadOver(dungeonDefinition);
		        });
        	}
        }
    }
    // Preload markers
    $.imagePreload(graphicsPack + '/static/images/markers/select.png', function() {
        $.displayDungeonLoadOver(dungeonDefinition);
    });
    $.imagePreload(graphicsPack + '/static/images/markers/selectcible.png', function() {
        $.displayDungeonLoadOver(dungeonDefinition);
    });
    $.runPreloading(function() {
        $.displayDungeonLoadOver(dungeonDefinition);
    });
}
$.fn.displayRoom = function(room) {
	var dungeonDefinition = currentDungeonDefinition;
    var ctx = this.get(0).getContext('2d');
    ctx.save();
    var roomPosX =room.position.x;
    var roomPosY =room.position.y;
    if (displayRotation == 1) {
    	var tmp = roomPosY;
    	roomPosY = roomPosX;
    	roomPosX = dungeonDefinition.size.height - tmp - 1	;
    } else if (displayRotation == 2) {
    	roomPosX = dungeonDefinition.size.width - roomPosX -1;
    	roomPosY = dungeonDefinition.size.height - roomPosY - 1;
    } else if (displayRotation == 3) {
		var tmp = roomPosY;
		roomPosY = dungeonDefinition.size.width - roomPosX - 1;
		roomPosX = tmp;
    }
    ctx.translate(((roomPosX*5+3.5)*referenceSize+selectBorderSize)*zoom, ((roomPosY*5+3.5)*referenceSize+selectBorderSize)*zoom);
    ctx.rotate(Math.PI / 2 * (room.rotation+displayRotation));
    ctx.translate(-((roomPosX*5+3.5)*referenceSize+selectBorderSize)*zoom, -((roomPosY*5+3.5)*referenceSize+selectBorderSize)*zoom);
    var url = graphicsPack + '/static/images/rooms/' + room.name + '.jpg';
    ctx.drawImage(imgs[url], ((roomPosX*5+1)*referenceSize+selectBorderSize)*zoom, ((roomPosY*5+1)*referenceSize+selectBorderSize)*zoom, 5*referenceSize*zoom, 5*referenceSize*zoom);
    // TODO: Markers
    ctx.restore();
}
$.fn.displaySlide = function(slide) {
	var dungeonDefinition = currentDungeonDefinition;
    var ctx = this.get(0).getContext('2d');
    var x = slide.position.x;
    var y = slide.position.y;
    if (displayRotation == 1) {
    	var tmp = y;
    	y = x;
    	x = dungeonDefinition.size.height*5+2 - tmp - (slide.direction == 'v' ? slide.size : 1);
    } else if (displayRotation == 2) {
    	x = dungeonDefinition.size.width*5+2 - x - (slide.direction == 'h' ? slide.size : 1);
    	y = dungeonDefinition.size.height*5+2 - y - (slide.direction == 'v' ? slide.size : 1);
    } else if (displayRotation == 3) {
		var tmp = y;
		y = dungeonDefinition.size.width*5+2 - x - (slide.direction == 'h' ? slide.size : 1);
		x = tmp;
    }
    var urlSlide = graphicsPack + '/static/images/rooms/reglette.jpg';
    for (var decalage = 0; decalage < slide.size; decalage++) {
        ctx.drawImage(imgs[urlSlide], (x*referenceSize+selectBorderSize)*zoom, (y*referenceSize+selectBorderSize)*zoom, referenceSize*zoom, referenceSize*zoom);
        if (slide.size == 5 && decalage != 2 || slide.size == 10 && (decalage == 1 || decalage == 3 || decalage == 6 || decalage == 8)) {
            var url = graphicsPack + '/static/images/rooms/reglette-' + slide.color + '.png';
            ctx.drawImage(imgs[url], ((x+0.25)*referenceSize+selectBorderSize)*zoom, ((y+0.25)*referenceSize+selectBorderSize)*zoom, referenceSize/2*zoom, referenceSize/2*zoom);
        }
        if (slide.direction == 'h' && displayRotation % 2 == 0 || slide.direction == 'v' && displayRotation % 2 == 1) {
            x++;
        } else {
            y++;
        }
    }
}
$.fn.displaySpawns = function(x, y, spawnsList) {
	var dungeonDefinition = currentDungeonDefinition;
    var ctx = this.get(0).getContext('2d');
    if (displayRotation == 1) {
    	var tmp = y;
    	y = x;
    	x = dungeonDefinition.size.height*5+2 - tmp - 1;
    } else if (displayRotation == 2) {
    	x = dungeonDefinition.size.width*5+2 - x - 1;
    	y = dungeonDefinition.size.height*5+2 - y - 1;
    } else if (displayRotation == 3) {
		var tmp = y;
		y = dungeonDefinition.size.width*5+2 - x - 1;
		x = tmp;
    }
    if (spawnsList.length == 1) {
        var url = graphicsPack + '/static/images/spawns/fond-' + spawnsList[0].color + '.png';
        var spawnSize = (referenceSize-spawnReduction)*zoom;
        var left = (x*referenceSize+spawnReduction/2+selectBorderSize)*zoom;
        var top = (y*referenceSize+spawnReduction/2+selectBorderSize)*zoom;
        ctx.drawImage(imgs[url], left, top, spawnSize, spawnSize);
        var url = graphicsPack + '/static/images/spawns/' + spawnsList[0].name + '.png';
        ctx.drawImage(imgs[url], left, top, spawnSize, spawnSize);
        for (var i in spawnsList[0].states) { var state = spawnsList[0].states[i]; 
	        if (state == 'consecrated' || state == 'undead' || state == 'bonusdefense' || state == 'bonusattaque' || state == 'noout' || state == 'cursed' || state == 'acidified' || state == 'poisoned' || state == 'hurt' || state == 'knocked' || state == 'tired' || state == 'freezed') {
	        	var url = graphicsPack + '/static/images/markers/' + state + '.png';
	        	ctx.drawImage(imgs[url], left, top, spawnSize, spawnSize);
	        }
        }
    } else if (spawnsList.length == 2) {
        // TODO: Display 2 characters
    } else {
        // Only the three first are considered
        // TODO display 3 charaters
    }
}
$.fn.displayPositionCase = function(xr, yr, x, y) {
	var dungeonDefinition = currentDungeonDefinition;
    var ctx = this.get(0).getContext('2d');
    var url = graphicsPack + '/static/images/rooms/position_' + (y*5+x+1) + '.png';
    x = xr*5+x+1;
    y = yr*5+y+1;
    if (displayRotation == 1) {
    	var tmp = y;
    	y = x;
    	x = dungeonDefinition.size.height*5+2 - tmp - 1;
    } else if (displayRotation == 2) {
    	x = dungeonDefinition.size.width*5+2 - x - 1;
    	y = dungeonDefinition.size.height*5+2 - y - 1;
    } else if (displayRotation == 3) {
		var tmp = y;
		y = dungeonDefinition.size.width*5+2 - x - 1;
		x = tmp;
    }
    var left = (x*referenceSize+spawnReduction/2+selectBorderSize-10*0.8)*zoom;
    var top = (y*referenceSize+spawnReduction/2+selectBorderSize+5*0.8)*zoom;
    ctx.drawImage(imgs[url], left, top, 100*zoom*0.8, 70*zoom*0.8);
}
$.fn.displayPositionRoom = function(room) {
	var dungeonDefinition = currentDungeonDefinition;
    var ctx = this.get(0).getContext('2d');
    ctx.save();
    var roomPosX =room.position.x;
    var roomPosY =room.position.y;
    var pos1 = String.fromCharCode(97+room.position.x);
    var pos2 = String.fromCharCode(97+room.position.y);
    if (displayRotation == 1) {
    	var tmp = roomPosY;
    	roomPosY = roomPosX;
    	roomPosX = dungeonDefinition.size.height - tmp - 1	;
    } else if (displayRotation == 2) {
    	roomPosX = dungeonDefinition.size.width - roomPosX -1;
    	roomPosY = dungeonDefinition.size.height - roomPosY - 1;
    } else if (displayRotation == 3) {
		var tmp = roomPosY;
		roomPosY = dungeonDefinition.size.width - roomPosX - 1;
		roomPosX = tmp;
    }
    var url = graphicsPack + '/static/images/rooms/position_' + pos2 + '.png';
    ctx.drawImage(imgs[url], ((roomPosX*5+1)*referenceSize+selectBorderSize)*zoom, ((roomPosY*5+1)*referenceSize+selectBorderSize)*zoom, 5*referenceSize*zoom/2, 5*referenceSize*zoom);
    var url = graphicsPack + '/static/images/rooms/position_' + pos1 + '.png';
    ctx.drawImage(imgs[url], ((roomPosX*5+1)*referenceSize+selectBorderSize)*zoom+5*referenceSize*zoom/2+1, ((roomPosY*5+1)*referenceSize+selectBorderSize)*zoom, 5*referenceSize*zoom/2, 5*referenceSize*zoom);
    ctx.restore();
}
$.displayDungeonLoadOver = function() {
    var dungeonDefinition = currentDungeonDefinition;
    // Prepare canvas
    var canvasRooms = $('#dungeon_rooms');
    var canvasSpawns = $('#dungeon_spawns');
    var canvasSelect = $('#dungeon_select');
    var canvasPosition = $('#dungeon_position');
    var canvasAutre = $('#dungeon_autre');
    if (displayRotation % 2 == 1) {
	    var canvasWidth = ((dungeonDefinition.size.height*5+2)*referenceSize+selectBorderSize*2)*zoom;
	    var canvasHeight = ((dungeonDefinition.size.width*5+2)*referenceSize+selectBorderSize*2)*zoom;
    } else {
	    var canvasWidth = ((dungeonDefinition.size.width*5+2)*referenceSize+selectBorderSize*2)*zoom;
	    var canvasHeight = ((dungeonDefinition.size.height*5+2)*referenceSize+selectBorderSize*2)*zoom;
    }
    canvasRooms.attr('width', canvasWidth);
    canvasRooms.attr('height', canvasHeight);
    canvasSpawns.attr('width', canvasWidth);
    canvasSpawns.attr('height', canvasHeight);
    canvasSelect.attr('width', canvasWidth);
    canvasSelect.attr('height', canvasHeight);
    canvasPosition.attr('width', canvasWidth);
    canvasPosition.attr('height', canvasHeight);
    canvasAutre.attr('height', canvasHeight);
    canvasAutre.attr('height', canvasHeight);
    // Display Rooms
    for (var i in dungeonDefinition.rooms) { var room = dungeonDefinition.rooms[i]
        canvasRooms.displayRoom(room);
    }
    // Display Slides
    for (var i in dungeonDefinition.slides) { var slide = dungeonDefinition.slides[i];
        canvasRooms.displaySlide(slide);
    }
    // Display characters (they are first sorted to check out the number of spawn by case)
    var spawnsArray = new Array();
    for (var i in dungeonDefinition.spawns) { var spawn = dungeonDefinition.spawns[i];
        var position = { x: spawn.position.x, y: spawn.position.y };
        if (spawn.room) {
            position.x += 1+spawn.room.x*5;
            position.y += 1+spawn.room.y*5;
        }
        if (!spawnsArray[position.y]) {
            spawnsArray[position.y] = new Array();
        }
        if (!spawnsArray[position.y][position.x]) {
            spawnsArray[position.y][position.x] = new Array();
        }
        spawnsArray[position.y][position.x][spawnsArray[position.y][position.x].length] = spawn;
    }
    for (var y in spawnsArray) { for (var x in spawnsArray[y]) {
        canvasSpawns.displaySpawns(x, y, spawnsArray[y][x]);
    }}
    // Run animation to show
    progressbarDialog.destroy();
    canvasRooms.show();
    canvasSpawns.show();
    $.displayPosition();
    canvasSelect.displayCurrentSelect();
}

/**
 * Display select
 */
var selectMode = 0; // 0: mode normal src+target), 1: mode src (only src), 2: (src + action)
var locationSrc = 0;
var locationDst = 0;
$.fn.displaySelect = function(location) {
	var dungeonDefinition = currentDungeonDefinition;
	// check location is not outside labyrinthe
	for (var sn in dungeonDefinition.slides) { var slide = dungeonDefinition.slides[sn];
		var x = slide.position.x;
	    var y = slide.position.y;
	    if (displayRotation == 1) {
	    	var tmp = y;
	    	y = x;
	    	x = dungeonDefinition.size.height*5+2 - tmp - (slide.direction == 'v' ? slide.size : 1);
	    } else if (displayRotation == 2) {
	    	x = dungeonDefinition.size.width*5+2 - x - (slide.direction == 'h' ? slide.size : 1);
	    	y = dungeonDefinition.size.height*5+2 - y - (slide.direction == 'v' ? slide.size : 1);
	    } else if (displayRotation == 3) {
			var tmp = y;
			y = dungeonDefinition.size.width*5+2 - x - (slide.direction == 'h' ? slide.size : 1);
			x = tmp;
	    }
	    var found = 0;
	    for (var decalage = 0; decalage < slide.size; decalage++) {
	       if (location.x == x && location.y == y) {
	    	   found = 1;
	    	   break;
	       }
	        if (slide.direction == 'h' && displayRotation % 2 == 0 || slide.direction == 'v' && displayRotation % 2 == 1) {
	            x++;
	        } else {
	            y++;
	        }
	    }
	    if (found == 1) {
	    	location.color = slide.color;
	    	break;
	    }
	}
	if (found == 0) {
		var roomnum = Math.floor((location.x-1)/5) + Math.floor((location.y-1)/5)*(displayRotation%2 == 1 ? dungeonDefinition.size.height : dungeonDefinition.size.width);
		if (!dungeonDefinition.rooms[roomnum]) {
			return;
		}
	}
	// Use location according to context
    var ctx = this.get(0).getContext('2d');
    var selectSize = (referenceSize+selectBorderSize*2-18)*zoom;
    if (locationSrc != 0 && location.x == locationSrc.x && location.y == locationSrc.y) {
    	ctx.clearRect((locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
    	locationSrc = locationDst;
    	locationDst = 0;
    	var selectUrl = graphicsPack + '/static/images/markers/select.png';
    	location = locationSrc;
    } else if (locationDst != 0 && location.x == locationDst.x && location.y == locationDst.y) {
    	ctx.clearRect((locationDst.x*referenceSize+9)*zoom, (locationDst.y*referenceSize+9)*zoom, selectSize, selectSize);
    	locationDst = 0;
    	location = 0;
    	var selectUrl = graphicsPack + '/static/images/markers/select.png';
    } else {
    	if (locationSrc != 0) {
    		if (selectMode == 0) {
		    	if (locationDst != 0) {
		    		ctx.clearRect((locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
		    		locationSrc = locationDst;
					ctx.clearRect((locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
			    	var selectUrl = graphicsPack + '/static/images/markers/select.png';
			    	ctx.drawImage(imgs[selectUrl], (locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
		    	}
		    	locationDst = location;
		    	selectUrl = graphicsPack + '/static/images/markers/selectcible.png';
    		} else if (selectMode == 1) {
	    		ctx.clearRect((locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
		    	locationSrc = location;
		    	selectUrl = graphicsPack + '/static/images/markers/select.png';    			
    		} else {
    			//TODO: run action on src + location as target
    		}
    	} else {
    		locationSrc = location;
    		selectUrl = graphicsPack + '/static/images/markers/select.png';
    	}
    }
	if (location != 0) {
		ctx.clearRect((location.x*referenceSize+9)*zoom, (location.y*referenceSize+9)*zoom, selectSize, selectSize);
    	ctx.drawImage(imgs[selectUrl], (location.x*referenceSize+9)*zoom, (location.y*referenceSize+9)*zoom, selectSize, selectSize);
	}
	updateAction();
}
$.fn.displayCurrentSelect = function(location) {
    var ctx = this.get(0).getContext('2d');
    var selectSize = (referenceSize+selectBorderSize*2-18)*zoom;
	if (locationSrc != 0) {
		var selectUrl = graphicsPack + '/static/images/markers/select.png';
    	ctx.drawImage(imgs[selectUrl], (locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
	}
	if (locationDst != 0) {
		var selectUrl = graphicsPack + '/static/images/markers/selectcible.png';
    	ctx.drawImage(imgs[selectUrl], (locationDst.x*referenceSize+9)*zoom, (locationDst.y*referenceSize+9)*zoom, selectSize, selectSize);
	}
}
$.fn.clearCurrentSelect = function(location) {
    var ctx = this.get(0).getContext('2d');
    var selectSize = (referenceSize+selectBorderSize*2-18)*zoom;
	if (locationSrc != 0) {
		ctx.clearRect((locationSrc.x*referenceSize+9)*zoom, (locationSrc.y*referenceSize+9)*zoom, selectSize, selectSize);
		locationSrc = 0;
	}
	if (locationDst != 0) {
		ctx.clearRect((locationDst.x*referenceSize+9)*zoom, (locationDst.y*referenceSize+9)*zoom, selectSize, selectSize);
		locationDst = 0;
	}
}

/** Transforme une position en lettre et chiffre */
function locationToString(locationget) {
	if (locationget == 0) return '0';
	var dungeonDefinition = currentDungeonDefinition;
	// Rotate location back
	loc = { x: locationget.x, y: locationget.y };
	if (displayRotation == 1) {
		var tmp = loc.y;
		loc.y = dungeonDefinition.size.width*5+2 - loc.x - 1;
		loc.x = tmp;
	} else if (displayRotation == 2) {
		loc.x = dungeonDefinition.size.width*5+2 - loc.x;
		loc.y = dungeonDefinition.size.height*5+2 - loc.y;
	} else if (displayRotation == 3) {
		var tmp = location.y;
		loc.y = loc.x;
		loc.x = dungeonDefinition.size.height*5+2 - tmp - 1;
	}
	var dungeonDefinition = currentDungeonDefinition;
	if (loc.x ==0 || loc.x == (displayRotation%2 == 1 ? dungeonDefinition.size.height : dungeonDefinition.size.width)*5+1 || loc.y ==0 || loc.y == (displayRotation%2 == 0 ? dungeonDefinition.size.height : dungeonDefinition.size.width)*5+1) {
		var roomstring = translate('REGLETTE') + ' ' + locationget.color;
		position = '';
	} else {
		room = {x: Math.floor((loc.x-1)/5), y: Math.floor((loc.y-1)/5)};
		roomnum = room.x + room.y*(displayRotation%2 == 1 ? dungeonDefinition.size.height : dungeonDefinition.size.width);
		if (dungeonDefinition.rooms[roomnum]) {
			position = loc.x-room.x*5 + (loc.y-room.y*5-1)*5;
			var roomstring = '' + String.fromCharCode(65+room.y) + String.fromCharCode(65+room.x);
		} else {
			var roomstring = 'r';
			position = loc.x + (loc.y)*5;
		}
	}
    return roomstring + position; 
}

function locationToStringRotate(locationget) {
	if (locationget == 0) return '0';
	var dungeonDefinition = currentDungeonDefinition;
	// Rotate location back
	loc = { x: locationget.x, y: locationget.y };
	if (displayRotation == 1) {
		var tmp = loc.y;
		loc.y = dungeonDefinition.size.width*5+2 - loc.x - 1;
		loc.x = tmp;
	} else if (displayRotation == 2) {
		loc.x = dungeonDefinition.size.width*5+2 - loc.x;
		loc.y = dungeonDefinition.size.height*5+2 - loc.y;
	} else if (displayRotation == 3) {
		var tmp = location.y;
		loc.y = loc.x;
		loc.x = dungeonDefinition.size.height*5+2 - tmp - 1;
	}
	return loc.x + ',' + loc.y
}

/** Permet la mise à jour des actions en fonction des cases sélectionnées */
function updateAction() {
	$('#actionsdialog').dialog('open', true);
	$('#actionsdialog').dialog('option', 'title', translate('ACTION_LOADING'));
	$('#actionsdialog').html('<center><img border="0" src="/static/images/interface/loading.gif"/><br/>Chargement des actions...</center>');
	$.get('/game/actions/' + locationToStringRotate(locationSrc) + '/' + locationToStringRotate(locationDst) + '/0', function(content) {
		var actions = eval('(' + content + ')');
		updateAction_callback(actions); 
	})
}


var padlink = '';
if (tablettepc) padlink = '&nbsp;<img style="vertical-align: middle" src="/static/images/interface/greenarrows.png" usemap="#mappad"/>';
function movewindows(direction) {
	var depval = 100;
	var offset = $('#actionsdialog').closest('.ui-dialog').offset();
	if (direction == 0) {
		offset.top -= depval;
	} else if (direction == 1) {
		offset.left += depval;
	} else if (direction == 2) {
		offset.top += depval;
	} else if (direction == 3) {
		offset.left -= depval;
	}
	$('#actionsdialog').closest('.ui-dialog').offset(offset);
}

/** Fonction de mise à jour des actions disponibles */
function updateAction_callback(actions) {
    if (locationSrc == 0) {
    	$('#actionsdialog').dialog('option', 'title', translate('ACTION_GENERIC') + padlink);
    } else if (locationDst == 0) {
    	$('#actionsdialog').dialog('option', 'title', translate('ACTION_ON_CASE').replace('{1}', locationToString(locationSrc)) + padlink);
    } else {
    	$('#actionsdialog').dialog('option', 'title', translate('ACTION_FROM_CASE_TO_CASE').replace('{1}', locationToString(locationSrc)).replace('{2}', locationToString(locationDst)) + padlink);
    }
    $('#actionsdialog').html('');
    for (var i in actions) { var action = actions[i];
    	var content = $("<div class=\"iconcontainer\"><img class=\"pointer icon\" title=\"" + action['title'] + "\" alt=\"" + action['title'] + "\" src=\"/static/images/actions/" + action['icon'] + ".gif\"/></div>");
    	content.click(action['callback']);
    	$('#actionsdialog').append(content);
    }
}

/** Lance une URL (action) */
function callurl(url) {
	// TODO: run callback
	alert('Run url : ' + url);
	$('#dungeon_select').clearCurrentSelect();
}
