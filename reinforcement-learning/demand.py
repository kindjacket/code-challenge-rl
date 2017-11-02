# from sim import Sim
from settings import Settings
from spatial_utils import distance


class RandomNumberGenerator:
    def __init__(self, seed):
        self.seed = 2345678901 + seed
        self.A = 48271
        self.M = 2147483647
        self.Q = self.M / self.A
        self.R = self.M % self.A
        self.one_over_M = 1.0 / self.M
        # self.next = self.next_random_number()

    def next_random_number(self):
        hi = self.seed / self.Q
        lo = self.seed % self.Q
        test = self.A * lo - self.R * hi
        if test > 0:
            self.seed = test
        else:
            self.seed = test + self.M
        return self.seed * self.one_over_M


def rand(min, max):
    return round((max - min) * random_number_generator.next_random_number() + min)


random_number_generator = RandomNumberGenerator(Settings.SEED)
names = ['john', 'clement', 'mike', 'arnaud']


class Person:
    def __init__(self, state):
        building_count = len(state.buildings)
        origin = state.buildings[rand(0, building_count - 1)]
        destination = state.buildings[rand(0, building_count - 1)]
        while destination.name == origin.name:
            destination = state.buildings[rand(0, building_count - 1)]
        name = names[rand(0, len(names) - 1)]
        dist = distance(origin, destination)
        time_people = dist * Settings.PEOPLE_SPEED + rand(Settings.WAIT_OF_PEOPLE_MIN, Settings.WAIT_OF_PEOPLE_MAX)
        self.name = name + str(state.current_people_index)
        state.current_people_index += 1
        self.x = origin.x
        self.y = origin.y
        self.origin = origin
        self.destination = destination
        self.time = time_people
        self.time0 = time_people
        self.vehicle = None
