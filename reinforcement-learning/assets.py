class Vehicle:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.passengers = []
        self.picks = []

    def pick(self, customer):
        self.picks.append(customer)

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1


class Building:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
