### forcing myself not to change the fundamentals of the sim

### assumptions

# 1. going direct to destination is optimal
# 2. changing destination mid route is sub optimal
# 3. picking a customer up takes a go. This needs to be tested
# 4. assume it's never optimal to wait at the beginning

### action space


# if not at destination:
    # if at sim start -
        # 1. move to new location
        # 2. wait
    # 1. continue on current route
    # 2. change route - probably ignore this to start with
# if at destination:
    # 1. wait
    # 2. pickup customer or customers @ location
    # 3. move to new location
from spatial_utils import move_to_absolute


def vehicle_at_building_check(vehicle, state):
    for building in state.buildings:
        if vehicle.x == building.x and vehicle.y == building.y:
            return building
    return 'not at building'


def get_action_space(state):
    # TODO - deal with start case if the vehicle waits. start.time = 0 is not good enough
    vehicle_actions = {}
    ### starting actions
    if state.time == 0:
        starting_actions = []
        for building in state.buildings:
            starting_actions.append(building.name)
        for vehicle in state.vehicles:
            vehicle_actions[vehicle.name] = starting_actions
    else:
        ### determine whether vehicle at building. This could be nicer but don't want to change sim fundamentals
        for vehicle in state.vehicles:
            vehicle_actions[vehicle.name] = []
            vehicle_at_building = vehicle_at_building_check(vehicle, state)
            if vehicle_at_building != 'not at building':
                ### adds buildings except the one the vec is at to possible actions
                for building in state.buildings:
                    if building != vehicle_at_building:
                        vehicle_actions[vehicle.name].append(building.name)
                vehicle_actions[vehicle.name].append('wait')
                ### adds customers at current vec location to possible action
                for customer in state.customers:
                    if customer.x == vehicle.x and customer.y == vehicle.y and customer not in vehicle.picks:
                        vehicle_actions[vehicle.name].append(customer.name)
    return vehicle_actions