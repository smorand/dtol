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
var zoom = 1; // Zoom of the dungeon
var graphicsPack = ''; // Root directory or location for the image

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
var selectBorderSize = 10;
var currentDungeonDefinition = 0;
var progressbarDialog = 0;

/**
 * Initialization
 */
function init_game() {
    progressbarDialog = new Dialog('dialog_progressbar');
    $('#zoom_slider').slider({
        min: 1,
        max: 10,
        step: 1,
        range: true,
        slide: function(e, ui) {
            $.setZoom(ui.value/10.0);
        }
    });
    $('#zoom_slider a:first').hide();
    $('#dungeon_select').click(function(e) {
        // TODO : Detect button and what to do ?
        var height = $('#dungeon').attr('height')/(referenceSize*zoom);
        var width = $('#dungeon').attr('width')/(referenceSize*zoom);
        var positionMouse = $.getRelativePosition(e, 'dungeon_select');
        var res = { position: { x: Math.floor(positionMouse.x/(referenceSize*zoom)), y: Math.floor(positionMouse.y/(referenceSize*zoom)) } };
        if (res.position.x != 0 && res.position.x != width-1 && res.position.y != 0 && res.position.y != height-1) {
            res = { position: { x: (res.position.x-1)%5, y: (res.position.y-1)%5 }, room: { x: Math.floor((positionMouse.x-referenceSize*zoom)/(referenceSize*zoom*5)), y: Math.floor((positionMouse.y-referenceSize*zoom)/(referenceSize*zoom*5)) }};
        }
        // Select
        $('#dungeon_select').displaySelect(res);
    });
}


/**
 * Set zoom
 * @param newZoom New zoom
 */
$.setZoom = function(newZoom) {
    zoom = newZoom;
    $('#zoom_slider').slider('value', Math.round(zoom*10));
    if (currentDungeonDefinition) {
        $.displayDungeon();
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
        $.imagePreload(graphicsPack + '/static/images/spawns/fond-' + spawn.color + '.gif', function() {
            $.displayDungeonLoadOver(dungeonDefinition);
        });        
    }
    // Preload markers
    $.imagePreload(graphicsPack + '/static/images/markers/select.png', function() {
        $.displayDungeonLoadOver(dungeonDefinition);
    });
    $.runPreloading(function() {
        $.displayDungeonLoadOver(dungeonDefinition);
    });
}
$.fn.displayRoom = function(room) {
    var ctx = this.get(0).getContext('2d');
    ctx.save();
    ctx.translate(((room.position.x*5+3.5)*referenceSize+selectBorderSize)*zoom, ((room.position.y*5+3.5)*referenceSize+selectBorderSize)*zoom);
    ctx.rotate(Math.PI / 2 * room.rotation);
    ctx.translate(-((room.position.x*5+3.5)*referenceSize+selectBorderSize)*zoom, -((room.position.y*5+3.5)*referenceSize+selectBorderSize)*zoom);
    var url = graphicsPack + '/static/images/rooms/' + room.name + '.jpg';
    ctx.drawImage(imgs[url], ((room.position.x*5+1)*referenceSize+selectBorderSize)*zoom, ((room.position.y*5+1)*referenceSize+selectBorderSize)*zoom, 5*referenceSize*zoom, 5*referenceSize*zoom);
    // TODO: Markers
    ctx.restore();
}
$.fn.displaySlide = function(slide) {
    var ctx = this.get(0).getContext('2d');
    var x = slide.position.x;
    var y = slide.position.y;
    var urlSlide = graphicsPack + '/static/images/rooms/reglette.jpg';
    for (var decalage = 0; decalage < slide.size; decalage++) {
        ctx.drawImage(imgs[urlSlide], (x*referenceSize+selectBorderSize)*zoom, (y*referenceSize+selectBorderSize)*zoom, referenceSize*zoom, referenceSize*zoom);
        if (slide.size == 5 && decalage != 2 || slide.size == 10 && (decalage == 1 || decalage == 3 || decalage == 6 || decalage == 8)) {
            var url = graphicsPack + '/static/images/rooms/reglette-' + slide.color + '.png';
            ctx.drawImage(imgs[url], ((x+0.25)*referenceSize+selectBorderSize)*zoom, ((y+0.25)*referenceSize+selectBorderSize)*zoom, referenceSize/2*zoom, referenceSize/2*zoom);
        }
        if (slide.direction == 'h') {
            x++;
        } else {
            y++;
        }
    }
}
$.fn.displaySpawns = function(x, y, spawnsList) {
    //TODO Spawn states
    var ctx = this.get(0).getContext('2d');
    if (spawnsList.length == 1) {
        var url = graphicsPack + '/static/images/spawns/fond-' + spawnsList[0].color + '.gif';
        var spawnSize = (referenceSize-spawnReduction)*zoom;
        var left = (x*referenceSize+spawnReduction/2+selectBorderSize)*zoom;
        var top = (y*referenceSize+spawnReduction/2+selectBorderSize)*zoom;
        ctx.drawImage(imgs[url], left, top, spawnSize, spawnSize);
        var url = graphicsPack + '/static/images/spawns/' + spawnsList[0].name + '.png';
        ctx.drawImage(imgs[url], left, top, spawnSize, spawnSize);
    } else if (spawnsList.length == 2) {
        // TODO: Display 2 characters
    } else {
        // Only the three first are considered
        // TODO display 3 charaters
    }
}
$.displayDungeonLoadOver = function() {
    var dungeonDefinition = currentDungeonDefinition;
    // Prepare canvas
    var canvasRooms = $('#dungeon_rooms');
    var canvasSpawns = $('#dungeon_spawns');
    var canvasSelect = $('#dungeon_select');
    var canvasWidth = ((dungeonDefinition.size.width*5+2)*referenceSize+selectBorderSize*2)*zoom;
    var canvasHeight = ((dungeonDefinition.size.height*5+2)*referenceSize+selectBorderSize*2)*zoom;
    canvasRooms.attr('width', canvasWidth);
    canvasRooms.attr('height', canvasHeight);
    canvasSpawns.attr('width', canvasWidth);
    canvasSpawns.attr('height', canvasHeight);
    canvasSelect.attr('width', canvasWidth);
    canvasSelect.attr('height', canvasHeight);
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
}

/**
 * Display select
 */
var previousPosition = 0;
$.fn.displaySelect = function(location) {
    var ctx = this.get(0).getContext('2d');
    var selectSize = (referenceSize+selectBorderSize*2)*zoom;
    var selectUrl = graphicsPack + '/static/images/markers/select.png';
    var pos = { x: location.position.x, y: location.position.y };
    if (previousPosition) {
        ctx.clearRect(previousPosition.left, previousPosition.top, selectSize, selectSize);
    }
    if (location.room) {
        pos = { x: pos.x+location.room.x*5+1, y: pos.y+location.room.y*5+1 };
    }
    var left = (pos.x*referenceSize)*zoom;
    var top = (pos.y*referenceSize)*zoom;
    if (left != previousPosition.left || top != previousPosition.top) {
        previousPosition = { left: left, top: top };
        ctx.drawImage(imgs[selectUrl], left, top, selectSize, selectSize);
    } else {
        previousPosition = 0;
    }
}
