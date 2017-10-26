from assets import Vehicle, Building


class State:
    def __init__(self, number_of_initial_people):
        self.vehicles = [Vehicle('one', 1, 3),
                         Vehicle('two', 2, 3),
                         Vehicle('three', 3, 3),
                         Vehicle('four', 4, 3),
                         Vehicle('five', 5, 3)]
        self.peoples = []
        self.buildings = [Building('A', 15, 16),
                          Building('B', 5, 10),
                          Building('C', 23, 2),
                          Building('D', 23, 18),
                          Building('E', 17, 20),
                          Building('F', 2, 23),
                          Building('G', 16, 10)]

        for i in range(0,number_of_initial_people-1):


### how do we update the state??
