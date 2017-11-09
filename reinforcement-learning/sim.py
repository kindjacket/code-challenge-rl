import random

from action_space import get_action_space
from spatial_utils import move_to_absolute
from state import State

state = State()


# vehicle_destination_map = {}
# for vehicle in state.vehicles:
#     vehicle_destination_map[vehicle.name] = None


def handle_action_space(action_space, vehicles_map, buildings_map):
    for car, actions in action_space.items():
        if len(actions) == 0:
            print("vehicle {} is travelling to destination".format(car))
            return
        action = random.choice(actions)
        # do nothing (wait)
        if action == 'wait':
            print("vehicle {} is waiting".format(car))
            return
        # move to building
        if action in building_names:
            move_to_absolute(vehicles_map.get(car), buildings_map.get(action))
            print("vehicle {} is setting off for building {}".format(car, action))
            return
        # pick up customer
        if action in customer_names:
            vehicles_map.get(car).pick(customers_map.get(action))
            print("vehicle {} is picking up {}".format(car, action))
            return


building_names = [building.name for building in state.buildings]
buildings_map = {building.name: building for building in state.buildings}
vehicles_map = {vehicle.name: vehicle for vehicle in state.vehicles}

for i in range(1000):
    customer_names = [customer.name for customer in state.customers]
    customers_map = {customer.name: customer for customer in state.customers}
    action_space = get_action_space(state)
    handle_action_space(action_space, vehicles_map, buildings_map)
    state.loop()
