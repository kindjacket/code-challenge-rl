def move_to_absolute(mover, destination):
    if abs(mover.x - destination.x) > abs(mover.y - destination.y):
        if mover.x < destination.x:
            mover.x += 1
        elif mover.x > destination.x:
            mover.x -= 1
    else:
        if mover.y < destination.y:
            mover.y += 1
        elif mover.y > destination.y:
            mover.y -= 1


class Vehicle:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.peoples = []
        self.picks = []

    def pick(self, peopleName):
        if peopleName.name:
            peopleName = peopleName.name
            if self.picks.indexOf(peopleName) is -1:
                self.picks.append(peopleName)

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_to(self, destination):
        move_to_absolute(destination)


class Building:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
