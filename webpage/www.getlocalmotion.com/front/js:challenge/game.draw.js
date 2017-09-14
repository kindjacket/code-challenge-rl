var LMCodeChallenge = new function () {

    var canvas;
    var context;
    var origin;
    var editor;

    var WIDTH;//number of columns of the game
    var HEIGHT;//number of rows of the game
    var CANVAS_WIDTH = 1200;
    var CANVAS_HEIGHT = 640;
    var SIDE = 24;

    var images = {};
    var PEOPLE_NUMBER = 32;
    var wins = [];
    var happys = [];
    var unhappys = [];

    this.init = function (width, height, restart) {
        WIDTH = width;
        HEIGHT = height;
        var canvas = document.getElementById("canvas");
        context = canvas.getContext("2d");
        origin = {i: CANVAS_WIDTH / 2, j: CANVAS_HEIGHT - 12};

        //activate button
        var box = document.getElementById("box");
        document.getElementById("take_challenge").onclick = function () {
            var html = '<div id="editor">'
            html += 'function turn(vehicles,peoples,buildings){\n'
            html += '   //documentation can be found in the source\n'
            html += '   //Good luck :)\n'
            html += '}</div>'
            html += '<br/><div id="btn"><a class="btn btn-primary btn-lg btn-block" id="run">Run the code</a></div>'
            box.innerHTML = html;
            document.getElementById("run").onclick = function () {
                runUserCode(restart)
            };
            editor = ace.edit("editor");
            var JavaScriptMode = require("ace/mode/javascript").Mode;
            editor.getSession().setMode(new JavaScriptMode());
            editor.setShowPrintMargin(false);
        }

        //load images sources from the DOM, we do this so it's possible to save the
        //document offline and keep all the necessary images.
        var imageSrcs = {};
        var imgDiv = document.getElementById('imgs');
        for (var idx in imgDiv.children) {
            var element = imgDiv.children[idx];
            if (element.getAttribute) {
                var alias = element.getAttribute('img-alias');
                var src = element.getAttribute('src');
                imageSrcs[alias] = src;
            }
        }
        loadImages(imageSrcs, restart);
    };

    this.draw = function (state) {
        context.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        drawGrid();
        drawBuildings(state.buildings);
        drawVehicles(state.vehicles);
        drawPeoples(state.peoples);
        drawStats(state);


        drawAnimation(happys, 'happy');
        drawAnimation(unhappys, 'unhappy');
        drawAnimation(wins, 'dollar');
    };

    this.win = function (dollars) {
        var peoples = [];
        for (var p = 0; p < PEOPLE_NUMBER; p++) {
            peoples.push({});
        }
        animateWin(dollars, peoples);

        document.getElementById('box').style.display = 'none';
        document.getElementById('win').style.display = 'block';
        document.getElementById('submit').onclick = function () {
            submit(dollars);
        }
    };

    this.happyPeople = function (pos) {
        happys.push({
            x: pos.x,
            y: pos.y,
            time: 0
        });
    }
    this.sadPeople = function (pos) {
        unhappys.push({
            x: pos.x,
            y: pos.y,
            time: 0
        });
    }
    this.dollars = function (pos) {
        wins.push({
            x: pos.x,
            y: pos.y,
            time: 0
        });
    }

    this.crash = function () {
        drawOnlyText('An exception occured, check the logs');
    };

    //RUN USER CODE
    function runUserCode(callback) {
        var code = editor.session.getValue();
        var evaled = false;
        try {
            eval.call(window, code);
            evaled = true;
        }
        catch (ex) {
            drawOnlyText('Oh wow, check your code, \nlook in the console, \nsomething went awry');
        }
        if (evaled) {
            callback();
        }
    }

    //GRID
    function drawGrid() {
        //draw grid
        context.lineWidth = 1;
        context.strokeStyle = '#bdc3c7';
        for (var n = 0; n <= WIDTH; n++) {
            var px1 = ptToPx({x: n * SIDE, y: 0});
            var px2 = ptToPx({x: n * SIDE, y: HEIGHT * SIDE});
            line(px1, px2);
        }
        for (var m = 0; m <= HEIGHT; m++) {
            var px1 = ptToPx({x: 0, y: m * SIDE});
            var px2 = ptToPx({x: WIDTH * SIDE, y: m * SIDE});
            line(px1, px2);
        }
        context.fillStyle = '#aaa';
        context.font = 'bold 10px sans-serif';
        context.textBaseline = 'middle';
        context.textAlign = 'left';
        for (var n = 1; n <= WIDTH; n++) {
            text(ptToPx({x: n * SIDE - 8, y: -8}), '' + n);
        }
        context.textAlign = 'right';
        for (var m = 1; m <= HEIGHT; m++) {
            text(ptToPx({x: -8, y: m * SIDE - 8}), '' + m);
        }
        context.textAlign = 'center';
        text(ptToPx({x: -8, y: -8}), '0');
    }

    function drawBuildings(buildings) {
        context.fillStyle = '#2c3e50';
        for (var idx in buildings) {
            var building = buildings[idx];
            var px = posToPx(building);
            image(offset(px, -16, -32), 'building');
            image(offset(px, 20, 6), ('panel'));
            text(offset(px, 32, 16), building.name);
        }
    }

    function drawVehicles(vehicles) {
        context.font = '10px sans-serif';
        for (var idx in vehicles) {
            var vehicle = vehicles[idx];
            var px = posToPx(vehicle);
            image(offset(px, 0, 0), 'vehicle');

            text(offset(px, 16, -4), vehicle.name);
        }
    }

    function drawPeoples(peoples) {
        context.font = 'bold 14px sans-serif';
        context.fillStyle = '#7f8c8d';
        for (var idx in peoples) {
            var people = peoples[idx];
            var px = posToPx(people);
            image(offset(px, 0, 0), people.img);
            image(offset(px, 20, -20), 'bul');
            text(offset(px, 32, -8), people.destination);
        }
    }

    function drawStats(state) {
        context.textAlign = 'left';
        context.fillStyle = '#7f8c8d';
        context.font = 'bold 48px sans-serif';
        context.lineWidth = 2;
        context.fillText('$' + state.dollars, 60, CANVAS_HEIGHT - 80);
        context.font = 'bold 12px sans-serif';
        context.fillText('turns: ' + state.time, 60, CANVAS_HEIGHT - 40);
    }

    //WIN

    function animateWin(dollars, peoples) {
        drawOnlyText('$' + dollars + ' in 1000 turns! You win!');
        for (var idx in peoples) {
            idx = parseInt(idx, 10);
            var people = peoples[idx];
            var offsetY = 0;
            if (people.time !== undefined) {
                offsetY = Math.abs(people.time++ - 4);
                if (people.time > 7) {
                    people.time = undefined;
                }
            } else {
                if (Math.random() * 200 < 2) {
                    people.time = 0;
                }
            }
            var i = idx * 32 + 10 * 32;
            var j = 14 * 32;
            if (idx > 15) {
                i = idx * 32 + 10 * 32 - 16 * 32;
                j = 16 * 32;
            }
            image({i: i + 24, j: j - offsetY * 3}, 'people' + idx);
        }
        setTimeout(function () {
            animateWin(dollars, peoples);
        }, 50);
    }


    function submit(dollars) {
        var email = document.getElementById('email').value;
        if (email.indexOf('@') === -1) {
            alert('Please enter an e-mail so we can contact you back.');
            return;
        }
        var json = {
            code: editor.session.getValue(),
            email: email,
            dollars: dollars
        };

        var params = 'JSON=' + encodeURIComponent(JSON.stringify(json));
        var xhr;
        try {
            xhr = new ActiveXObject('Msxml2.XMLHTTP');
        }
        catch (e) {
            try {
                xhr = new ActiveXObject('Microsoft.XMLHTTP');
            }
            catch (e2) {
                try {
                    xhr = new XMLHttpRequest();
                }
                catch (e3) {
                    xhr = false;
                }
            }
        }
        xhr.open('POST', '/code-challenge', true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params);
        document.getElementById('win-title').innerHTML = 'Thank you!';
        document.getElementById('win-body').innerHTML = 'Check your emails';
    }


    //DRAW TOOLS
    function posToPx(pos) {
        return {
            i: Math.floor(SIDE * (pos.x - pos.y)) + origin.i,
            j: origin.j - Math.floor(SIDE * (pos.x + pos.y) / 2)
        }
    }

    function ptToPx(p) {
        return {
            i: Math.floor(p.x - p.y) + origin.i,
            j: origin.j - Math.floor((p.x + p.y) / 2)
        }
    }

    function offset(px, offsetI, offsetJ) {
        return {i: px.i + offsetI, j: px.j + offsetJ};
    }

    function line(a, b) {
        if (a.i == b.i) {
            a.i += 0.5;
            b.i += 0.5;
        }
        if (a.j == b.j) {
            b.j += 0.5;
            a.j += 0.5;
        }
        context.beginPath();
        context.moveTo(a.i, a.j);
        context.lineTo(b.i, b.j);
        context.stroke();
    }

    function text(px, text) {
        context.fillText(text, px.i, px.j);
    }

    function image(px, imgAlias) {
        context.drawImage(images[imgAlias], px.i, px.j);
    }

    function drawOnlyText(txt) {
        context.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        context.textAlign = 'center';
        context.fillStyle = '#7f8c8d';
        context.font = 'bold 30px sans-serif';
        context.fillText(txt, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 3);
    }

    function drawAnimation(array, img) {
        for (var idx = 0; idx < array.length; idx++) {
            var obj = array[idx];
            var px = posToPx(obj);
            image(offset(px, 8, -obj.time * 4), img);
            obj.time++;
            if (obj.time > 10) {
                array.splice(idx--, 1);
            }
        }
    }

    function loadImages(sources, callback) {
        var loadedImages = 0;
        var numImages = 0;
        for (var src in sources) {
            numImages++;
        }
        for (var src in sources) {
            images[src] = new Image();
            images[src].onload = function () {
                if (++loadedImages >= numImages) {
                    callback();
                }
            };
            images[src].src = sources[src];
        }
    }
}();