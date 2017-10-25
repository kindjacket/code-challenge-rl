import math

time = 0
dollars = 0

WIDTH = 24  # number of columns of the game
HEIGHT = 24  # number of rows of the game
PEOPLE_SPEED = 2  # number of turns it takes to a people to move 1px
PEOPLE_GENERATION = 3  # a new people is generated every x turns
NUMBER_OF_INITIAL_PEOPLES = 10  # number of people at the begining of the game
WAIT_OF_PEOPLE_MIN = 25  # number of turns a people will wait before leaving the building
WAIT_OF_PEOPLE_MAX = 50
SPEED = 1 / 50  # higher = faster
SEED = 0  # random generation seed

currentPeopleIndex = 0
names = ['john', 'clement', 'mike', 'arnaud']

# currentTimeoutId what does this do??
locked = False


def loop(state):
    try:
        oldState = state
        state = copy(state)
        state.time = time
        state.dollars = dollars
        # we're not drawing anything so don't need this
        # LMCodeChallenge.draw(state); // draw

        decorate(state)
        turn(state.vehicles, state.peoples, state.buildings)

        unsane = sanityCheck(oldState, state)
        if (unsane):
            raise Exception('did not work right')
        return
        move(state)

        ## probs remove this part and store score
        if time == 1000 and dollars >= 10000:
            print('good score - you bloody blood legend')
        return None

        # adds new people
        if time % PEOPLE_GENERATION == 0:
            generatePeople(state)

        time += 1
        if locked:
            return
        currentTimeoutId = setTimeout(function()
        1 / SPEED
}
catch(ex)
{
LMCodeChallenge.crash();
throw
ex; // will
not keep
the
stacktrace in chrome, it
's a bug.


def sanityCheck(oldState, newState):
    if oldState.buildings.length is not newState.buildings.length)
    return 'The number of buildings have changed !'
    if oldState.vehicles.length is not newState.vehicles.length)
    return 'The number of vehicles has changed!'
    if oldState.peoples.length is not newState.peoples.length)
    return 'The number of people has changed!'

    for var idx in oldState.buildings:
        var
        oldBuilding = oldState.buildings[idx]
        var
        newBuilding = newState.buildings[idx]
        if distance(oldBuilding, newBuilding) > 0)
        return 'A building has moved'
    }

    for var idx in oldState.vehicles:
        var
    oldVehicle = oldState.vehicles[idx]
    var
    newVehicle = newState.vehicles[idx]
    if newVehicle.peoples.length > 4) return 'A vehicle is filled with more than 4 people'
    if newVehicle.peoples.length is not oldVehicle.peoples.length)
    return 'People will hop on vehicles by themselves. Do not try to force them.'
    if distance(oldVehicle, newVehicle) > 1)
    return 'A vehicle moved of more than 1px (diagonal moves are not allowed)'
    for var idx2 in newVehicle.people:
        var
        oldVPeople = oldVehicle.peoples[idx2]
        var
        newVPeople = newVehicle.peoples[idx2]
        if oldVPeople.time < newVPeople.time)
        return 'One of the people had his time messed up'
    }
    }

    for var idx in oldState.peoples:
        var
    oldPeople = oldState.peoples[idx]
    var
    newPeople = newState.peoples[idx]
    if oldPeople.time < newPeople.time) return 'One of the people had his time messed up'
    if not oldPeople.vehicle and not newPeople.vehicle and distance(oldPeople, newPeople) > 0)
    return 'You moved a people (you should not)'

}
return False
}

### this moves the vehicle
def decorate(state):
    for vec in state.vehicles:
        vehicle.moveUp = moveUp
        vehicle.moveDown = moveDown
        vehicle.moveLeft = moveLeft
        vehicle.moveRight = moveRight
        vehicle.moveTo = moveTo
        vehicle.pick = pick


### this does something with the state. Why do we need this?
def undecorate(state):
    for var idx in state.vehicles:
        var
        vehicle = state.vehicles[idx]
        del vehicle.moveUp
        del vehicle.moveDown
        del vehicle.moveLeft
        del vehicle.moveRight
        del vehicle.moveTo
        del vehicle.pick


def pick(peopleName):
    var
    vehicle = this
    if peopleName.name:
        peopleName = peopleName.name; // safety
        check:)

        if vehicle.picks.indexOf(peopleName) is -1:
            vehicle.picks.append(peopleName)


def moveUp():
    this.y - -


def moveDown():
    this.y + +


def moveLeft():
    this.x - -


def moveRight():
    this.x + +


def moveTo(destination):
    moveToAbsolute(this, destination)


def moveToAbsolute(mover, destination):
    if Math.abs(mover.x - destination.x) > Math.abs(mover.y - destination.y):
        if mover.x < destination.x:
            mover.x + +

        else if mover.x > destination.x:
            mover.x - -


    else {
    if mover.y < destination.y:
        mover.y + +

    else if mover.y > destination.y:
        mover.y - -

    }


    def move(state):
        // drop & pickup
        people
        for var idx in state.vehicles:
            var
            vehicle = state.vehicles[idx]

            // find if the
            vehicle is in a
            building
            var
            building = None
            for var idx2 in state.buildings:
                var
                buildingCandidate = state.buildings[idx2]
                if distance(buildingCandidate, vehicle) is 0:
                    building = buildingCandidate

            if building:
                // drop
                people
                off
                for var idx3 = 0; idx3 < vehicle.peoples.length; idx3++:
                    var
                    passenger = vehicle.peoples[idx3]
                    if passenger.destination is building.name:
                        vehicle.peoples.splice(idx3 - -, 1)
                        passenger.vehicle = Unset
                        if passenger.time > 0:
                            log(
                                '' + passenger.name + ' was dropped off vehicle ' + vehicle.name + ' yay! +$50 time left:' + passenger.time + '/' + passenger.time0)
                            // earn
                            dollars
                            LMCodeChallenge.dollars(vehicle)
                            dollars += 50

                        else {
                        log('' + passenger.name + ' was dropped off vehicle ' + vehicle.name + ' but was ' + (-passenger.time) + ' late :(')
                        LMCodeChallenge.sadPeople(vehicle)
                        }

                // pick
                people
                up
                for var idx3 = 0; idx3 < state.peoples.length; idx3++:
                    var
                    people = state.peoples[idx3]
                    if people.origin is building.name:
                        var
                        idxPinV = vehicle.picks.indexOf(people.name)
                        if distance(people, building) is 0 and vehicle.peoples.length < 4 and idxPinV is not -1:
                            // hop
                            on
                            log('' + people.name + ' hoped on vehicle ' + vehicle.name)
                            vehicle.peoples.append(people)
                            vehicle.picks.splice(idxPinV, 1)
                            people.vehicle = vehicle.name
                            state.peoples.splice(idx3 - -, 1)
                            LMCodeChallenge.happyPeople(people)

            // empty
            the
            picks
            list
            vehicle.picks = []

            // decrease
            time
            of
            people in vehicle
            for var idx3 in vehicle.peoples:
                vehicle.peoples[idx3].time - -

        // move
        people
        for var idx = 0; idx < state.peoples.length; idx++:
            var
            people = state.peoples[idx]
            people.time - -
            var
            destination = getBuilding(people.destination, state.buildings)
            var
            origin = getBuilding(people.origin, state.buildings)

            if distance(people, destination) is 0:
                // remove
                from the game
                state.peoples.splice(idx - -, 1)
                LMCodeChallenge.sadPeople(people)

            else if PEOPLE_SPEED * distance(people, destination) >= people.time:
                if distance(people, origin) is 0:
                    // log(people.name + ' decided to walk to destination, cannot wait longer')

                moveToAbsolute(people, destination)

    def generatePeople(state):
        var
        origin = state.buildings[rand(0, state.buildings.length - 1)]
        var
        destination = state.buildings[rand(0, state.buildings.length - 1)]
        while destination.name is origin.name:
            destination = state.buildings[rand(0, state.buildings.length - 1)]

        var
        name = names[rand(0, names.length - 1)]
        var
        dist = distance(origin, destination)
        var
        timePeople = dist * PEOPLE_SPEED + rand(WAIT_OF_PEOPLE_MIN, WAIT_OF_PEOPLE_MAX)
        state.peoples.append({
            name: name + (currentPeopleIndex + +),
            x: origin.x,
            y: origin.y,
            origin: origin.name,
            destination: destination.name,
            time: timePeople,
            time0: timePeople,
            img: 'people' + rand(0, PEOPLE_NUMBER - 1)
        })

    def getBuilding(name, buildings):
        for var idx in buildings:
            var
            building = buildings[idx]
            if building.name is name:
                return building

        return None

    def getPeople(name, peoples):
        for var idx in peoples:
            if peoples[idx].name is name:
                return peoples[idx]

        return None

    def distance(a, b):
        return Math.abs(a.x - b.x) + Math.abs(a.y - b.y)

    def copy(state):
        return JSON.parse(JSON.stringify(state))

    def newVehicle(name, x, y):
        return {
            name: name,
            x: x,
            y: y,
            peoples: [],
            picks: []
        }

    def newBuilding(name, x, y):
        return {
            name: name,
            x: x,
            y: y
        }

    def log(txt):
        if typeof console is not 'undefined':
            print(txt)

    ### the random number generator is important to ensure consistency vs python ver and js ver
    def nextRandomNumber():
        var
        hi = this.seed / this.Q
        var
        lo = this.seed % this.Q
        var
        test = this.A * lo - this.R * hi
        if test > 0:
            this.seed = test
        else:
            this.seed = test + this.M

        return (this.seed * this.oneOverM)

    def RandomNumberGenerator(seed):
        seed = 2345678901 + seed
        A = 48271
        M = 2147483647
        Q = M / A
        R = M % A
        oneOverM = 1.0 / M
        next = nextRandomNumber
        return next

    def rand(Min, Max):
        return math.round((Max - Min) * randomNumberGenerator(seed) + Min)

    randomNumberGenerator = RandomNumberGenerator(SEED)

    // start
    the
    game
    window.onload =

    def():

        LMCodeChallenge.init(WIDTH, HEIGHT, restart)

    def init():
        state = {
            vehicles: [
                newVehicle('one', 1, 3),
                newVehicle('two', 2, 3),
                newVehicle('three', 3, 3),
                newVehicle('four', 4, 3),
                newVehicle('five', 5, 3)
            ],
            peoples: [],
            buildings: [
                newBuilding('A', 15, 16),
                newBuilding('B', 5, 10),
                newBuilding('C', 23, 2),
                newBuilding('D', 23, 18),
                newBuilding('E', 17, 20),
                newBuilding('F', 2, 23),
                newBuilding('G', 16, 10)
            ]
        }
        for var i = 0; i < NUMBER_OF_INITIAL_PEOPLES; i++:
            generatePeople(state)

        return state

    def restart():
        locked = True
        if currentTimeoutId) clearTimeout(currentTimeoutId)
        time = 0
        dollars = 0
        var state = init()
        locked = False
        loop(state)
