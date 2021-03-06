function turn(vehicles,peoples,buildings){};

(function(){
    //GLOBAL VARIABLE CONTAINING THE STATE OF THE GAME

    var time = 0;
    var dollars=0;

    var WIDTH=24;//number of columns of the game
    var HEIGHT=24;//number of rows of the game
    var PEOPLE_SPEED=2;//number of turns it takes to a people to move 1px
    var PEOPLE_GENERATION=3;//a new people is generated every x turns
    var NUMBER_OF_INITIAL_PEOPLES=10;//number of people at the begining of the game
    var WAIT_OF_PEOPLE_MIN=25;//number of turns a people will wait before leaving the building
    var WAIT_OF_PEOPLE_MAX=50;
    var SPEED = 1/50; //higher = faster

    var SEED = 0;//random generation seed

    //for drawing and stuffs
    var PEOPLE_NUMBER=32;//number of different drawings for the people
    var currentPeopleIndex = 0;
    var names = ['john','clement','mike','arnaud'];

    var currentTimeoutId;
    var locked = false;

    function loop(state){
        try{

            //copy the state to make some checks afterwards
            undecorate(state);
            var oldState = state;
            state = copy(state);


            state.time = time;
            state.dollars = dollars;
            LMCodeChallenge.draw(state);//draw just before player's turn

            decorate(state);//add helper functions
            turn(state.vehicles,state.peoples,state.buildings);

            var unsane = sanityCheck(oldState,state);
            if(unsane){
                log('UNSANE! '+unsane);
                LMCodeChallenge.crash();
                return;
            }
            move(state);

            if(time===1000 && dollars>=10000){
                LMCodeChallenge.win(dollars);
                return;
            }

            if(time%PEOPLE_GENERATION==0){
                //add new people
                generatePeople(state)
            }

            time++;
            if(locked)return;
            currentTimeoutId = setTimeout(function(){
                loop(state);
            },1/SPEED);
        }
        catch(ex){
            LMCodeChallenge.crash();
            throw ex; //will not keep the stacktrace in chrome, it's a bug.
        }
    }

    function sanityCheck(oldState,newState){
        if(oldState.buildings.length!==newState.buildings.length) return 'The number of buildings have changed !';
        if(oldState.vehicles.length!==newState.vehicles.length) return 'The number of vehicles has changed!';
        if(oldState.peoples.length!==newState.peoples.length) return 'The number of people has changed!';

        for(var idx in oldState.buildings){
            var oldBuilding = oldState.buildings[idx];
            var newBuilding = newState.buildings[idx];
            if(distance(oldBuilding,newBuilding)>0)return 'A building has moved';
        }

        for(var idx in oldState.vehicles){
            var oldVehicle = oldState.vehicles[idx];
            var newVehicle = newState.vehicles[idx];
            if(newVehicle.peoples.length>4)return 'A vehicle is filled with more than 4 people';
            if(newVehicle.peoples.length !== oldVehicle.peoples.length)return 'People will hop on vehicles by themselves. Do not try to force them.';
            if(distance(oldVehicle,newVehicle)>1)return 'A vehicle moved of more than 1px (diagonal moves are not allowed)';
            for(var idx2 in newVehicle.people){
                var oldVPeople = oldVehicle.peoples[idx2];
                var newVPeople = newVehicle.peoples[idx2];
                if(oldVPeople.time<newVPeople.time)return 'One of the people had his time messed up';
            }
        }

        for(var idx in oldState.peoples){
            var oldPeople = oldState.peoples[idx];
            var newPeople = newState.peoples[idx];
            if(oldPeople.time<newPeople.time)return 'One of the people had his time messed up';
            if(!oldPeople.vehicle && !newPeople.vehicle && distance(oldPeople,newPeople)>0)return 'You moved a people (you should not)';
        }
        return false;
    }

    function decorate(state){
        for(var idx in state.vehicles){
            var vehicle = state.vehicles[idx];
            vehicle.moveUp = moveUp;
            vehicle.moveDown = moveDown;
            vehicle.moveLeft = moveLeft;
            vehicle.moveRight = moveRight;
            vehicle.moveTo = moveTo;
            vehicle.pick = pick;
        }
    }
    function undecorate(state){
        for(var idx in state.vehicles){
            var vehicle = state.vehicles[idx];
            delete vehicle.moveUp;
            delete vehicle.moveDown;
            delete vehicle.moveLeft;
            delete vehicle.moveRight;
            delete vehicle.moveTo;
            delete vehicle.pick;
        }
    }
    function pick(peopleName){
        var vehicle = this;
        if(peopleName.name){
            peopleName = peopleName.name;//safety check :)
        }
        if(vehicle.picks.indexOf(peopleName)===-1){
            vehicle.picks.push(peopleName);
        }
    }
    function moveUp(){
        this.y--;
    }
    function moveDown(){
        this.y++;
    }
    function moveLeft(){
        this.x--;
    }
    function moveRight(){
        this.x++;
    }
    function moveTo(destination){
        moveToAbsolute(this,destination);
    }
    function moveToAbsolute(mover,destination){
        if(Math.abs(mover.x-destination.x)>Math.abs(mover.y-destination.y)){
            if(mover.x<destination.x){
                mover.x++;
            }
            else if(mover.x>destination.x){
                mover.x--;
            }
        }
        else{
            if(mover.y<destination.y){
                mover.y++;
            }
            else if(mover.y>destination.y){
                mover.y--;
            }
        }
    }

    function move(state){
        //drop & pickup people
        for(var idx in state.vehicles){
            var vehicle = state.vehicles[idx];

            //find if the vehicle is in a building
            var building=null;
            for(var idx2 in state.buildings){
                var buildingCandidate = state.buildings[idx2];
                if(distance(buildingCandidate,vehicle)===0){
                    building = buildingCandidate;
                }
            }

            if(building){
                //drop people off
                for(var idx3=0; idx3<vehicle.peoples.length;idx3++){
                    var passenger = vehicle.peoples[idx3];
                    if(passenger.destination === building.name){
                        vehicle.peoples.splice(idx3--,1);
                        passenger.vehicle = undefined;
                        if(passenger.time>0){
                            log(''+passenger.name+' was dropped off vehicle '+vehicle.name+' yay! +$50 time left:'+passenger.time+'/'+passenger.time0);
                            //earn dollars
                            LMCodeChallenge.dollars(vehicle);
                            dollars+=50;
                        }
                        else{
                            log(''+passenger.name+' was dropped off vehicle '+vehicle.name+' but was '+(-passenger.time)+' late :(');
                            LMCodeChallenge.sadPeople(vehicle);
                        }
                    }
                }

                //pick people up
                for(var idx3=0; idx3<state.peoples.length;idx3++){
                    var people = state.peoples[idx3];
                    if(people.origin === building.name){
                        var idxPinV = vehicle.picks.indexOf(people.name);
                        if(distance(people,building)===0 && vehicle.peoples.length<4 && idxPinV!==-1 ){
                            //hop on
                            log(''+people.name+' hoped on vehicle '+vehicle.name);
                            vehicle.peoples.push(people);
                            vehicle.picks.splice(idxPinV,1);
                            people.vehicle = vehicle.name;
                            state.peoples.splice(idx3--,1);
                            LMCodeChallenge.happyPeople(people);
                        }
                    }
                }
            }

            //empty the picks list
            vehicle.picks=[];

            //decrease time of people in vehicle
            for(var idx3 in vehicle.peoples){
                vehicle.peoples[idx3].time--;
            }
        }

        //move people
        for(var idx=0; idx<state.peoples.length;idx++){
            var people = state.peoples[idx];
            people.time --;
            var destination = getBuilding(people.destination,state.buildings);
            var origin = getBuilding(people.origin,state.buildings);

            if(distance(people,destination)===0){
                //remove from the game
                state.peoples.splice(idx--,1);
                LMCodeChallenge.sadPeople(people);
            }
            else if(PEOPLE_SPEED*distance(people,destination)>=people.time){
                if(distance(people,origin)===0){
                    //log(people.name+' decided to walk to destination, cannot wait longer');
                }
                moveToAbsolute(people,destination);
            }
        }
    }

    function generatePeople(state){
        var origin = state.buildings[rand(0,state.buildings.length-1)];
        var destination = state.buildings[rand(0,state.buildings.length-1)];
        while(destination.name === origin.name){
            destination = state.buildings[rand(0,state.buildings.length-1)];
        }
        var name = names[rand(0,names.length-1)];
        var dist = distance(origin,destination);
        var timePeople = dist*PEOPLE_SPEED + rand(WAIT_OF_PEOPLE_MIN,WAIT_OF_PEOPLE_MAX);
        state.peoples.push({
            name:name+(currentPeopleIndex++),
            x:origin.x,
            y:origin.y,
            origin:origin.name,
            destination:destination.name,
            time:timePeople,
            time0:timePeople,
            img:'people'+rand(0,PEOPLE_NUMBER-1)
        });
    }

    function getBuilding(name,buildings){
        for(var idx in buildings){
            var building = buildings[idx];
            if(building.name === name){
                return building;
            }
        }
        return null;
    }
    function getPeople(name,peoples){
        for(var idx in peoples){
            if(peoples[idx].name === name){
                return peoples[idx];
            }
        }
        return null;
    }

    function distance(a,b){
        return Math.abs(a.x-b.x)+Math.abs(a.y-b.y);
    }

    function copy(state){
        return JSON.parse(JSON.stringify(state));
    }

    function newVehicle(name,x,y){
        return {
            name:name,
            x:x,
            y:y,
            peoples:[],
            picks:[]
        };
    }

    function newBuilding(name,x,y){
        return {
            name:name,
            x:x,
            y:y
        };
    }

    function log(txt){
        if(typeof console !== 'undefined'){
            console.log(txt);
        }
    }

    //RANDOM NUMBER GENERATOR
    function nextRandomNumber(){
        var hi = this.seed / this.Q;
        var lo = this.seed % this.Q;
        var test = this.A * lo - this.R * hi;
        if(test > 0){
            this.seed = test;
        } else {
            this.seed = test + this.M;
        }
        return (this.seed * this.oneOverM);
    }
    function RandomNumberGenerator(seed){
        this.seed = 2345678901 + seed
        this.A = 48271;
        this.M = 2147483647;
        this.Q = this.M / this.A;
        this.R = this.M % this.A;
        this.oneOverM = 1.0 / this.M;
        this.next = nextRandomNumber;
        return this;
    }
    function rand(Min, Max){
        return Math.round((Max-Min) * randomNumberGenerator.next() + Min);
    }
    var randomNumberGenerator = new RandomNumberGenerator(SEED);


    //start the game
    window.onload = function() {

        LMCodeChallenge.init(WIDTH,HEIGHT,restart);
    }


    function init(){
        var state = {
            vehicles:[
                newVehicle('one',1,3),
                newVehicle('two',2,3),
                newVehicle('three',3,3),
                newVehicle('four',4,3),
                newVehicle('five',5,3)
            ],
            peoples:[],
            buildings:[
                newBuilding('A',15,16),
                newBuilding('B',5,10),
                newBuilding('C',23,2),
                newBuilding('D',23,18),
                newBuilding('E',17,20),
                newBuilding('F',2,23),
                newBuilding('G',16,10)
            ]
        };
        for(var i=0;i<NUMBER_OF_INITIAL_PEOPLES;i++){
            generatePeople(state);
        }
        return state;
    }

    function restart(){
        locked = true;
        if (currentTimeoutId) clearTimeout(currentTimeoutId);
        time = 0;
        dollars = 0;
        var state = init();
        locked = false;
        loop(state);

    }
})();


