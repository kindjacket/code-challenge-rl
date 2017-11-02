from assets import Vehicle, Building
from demand import Person
from settings import Settings
from spatial_utils import distance, move_to_absolute


class State:
    def __init__(self):
        self.time = 0
        self.dollars = 0
        self.vehicles = [Vehicle('one', 1, 3),
                         Vehicle('two', 2, 3),
                         Vehicle('three', 3, 3),
                         Vehicle('four', 4, 3),
                         Vehicle('five', 5, 3)]
        self.customers = []
        self.buildings = [Building('A', 15, 16),
                          Building('B', 5, 10),
                          Building('C', 23, 2),
                          Building('D', 23, 18),
                          Building('E', 17, 20),
                          Building('F', 2, 23),
                          Building('G', 16, 10)]
        self.current_people_index = 0
        self.dollars = 0
        for i in range(Settings.NUMBER_OF_INITIAL_PEOPLES):
            self.customers.append(Person(self))

    def move(self):
        ### why do we have picks and passengers???
        for vehicle in self.vehicles:

            ### find out if vehicle is at a building
            building = None
            for building_candidate in self.buildings:
                if distance(building_candidate, vehicle) == 0:
                    building = building_candidate

            if building is not None:
                ### auto drops people off
                for passenger in vehicle.passengers:
                    vehicle.passengers.remove(passenger)
                    passenger.vehicle = None
                    if passenger.time > 0:
                        print('{} was dropped off by vehicle {} yay! +$50 time left: {} / {}'.format(passenger.name,
                                                                                                     vehicle.name,
                                                                                                     passenger.time,
                                                                                                     passenger.time0))
                        self.dollars += 50
                    else:
                        print('{} was dropped off by vehicle {} but was {} late :('.format(passenger.name,
                                                                                           vehicle.name,
                                                                                           -passenger.time))

                ### picks people up
                for customer in self.customers:
                    if customer.origin == building:
                        ## dont't understand what this part does yet
                        ## var idxPinV = vehicle.picks.indexOf(people.name);
                        if distance(customer, building) == 0 \
                                and len(vehicle.passengers) < 4 \
                                and customer in vehicle.picks:
                            print('{} got into vehicle {}'.format(customer.name, vehicle.name))
                            vehicle.passengers.append(customer)
                            vehicle.picks.remove(customer)
                            customer.vehicle = vehicle.name
                            self.customers.remove(customer)

            ### empties pick list
            vehicle.picks = []
            for passenger in vehicle.passengers:
                passenger.time -= 1

        ### moves people
        for customer in self.customers:
            customer.time -= 1
            if distance(customer, customer.destination) == 0:
                ### removes customer from game (this is if the customer walks)
                self.customers.remove(customer)
            elif (Settings.PEOPLE_SPEED * distance(customer, customer.destination)) >= customer.time:
                move_to_absolute(customer, customer.destination)

    def loop(self):
        self.move()
        ## probs remove this part and store score
        if self.time == 1000 and self.dollars >= 10000:
            print('good score - you bloody blood legend')

        # adds new people
        if self.time % Settings.PEOPLE_GENERATION == 0:
            ### could maybe append in the Person generation part
            self.customers.append(Person(self))

        self.time += 1
