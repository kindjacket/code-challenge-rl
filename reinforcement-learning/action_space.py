### forcing myself not to change the fundamentals of the sim

### action space

# if not at destination:
    # 1. continue on current route
    # 2. change route
# if at destination:
    # 1. wait
    # 2. pickup customer or customers @ location
    # 3. move to new location

def vehicle_at_building_check(vehicle, state):
    for building in state.buildings:
        if vehicle.x == building.x and vehicle.y == building.y:
            return True
    return False


class ActionSpace:
    def __init__(self, state):
        ### determine whether vehicle at building. This could be nicer but don't want to change sim fundamentals
        for vehicle in state.vehicles:
            if vehicle_at_building_check(vehicle, state):
                1+1
            else:
