def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


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
